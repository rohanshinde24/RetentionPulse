"""Public API gateway for RetentionPulse."""
from __future__ import annotations

import asyncio
import csv
import io
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import httpx
import pandas as pd
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

from shared.schemas import CustomerData

PREDICT_URL = os.getenv("PREDICT_URL", "http://localhost:8001")
EXPLAIN_URL = os.getenv("EXPLAIN_URL", "http://localhost:8002")
DATA_PATH = Path(os.getenv("CUSTOMER_DATA_PATH", str(Path(__file__).resolve().parents[2] / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv")))
TIMEOUT = httpx.Timeout(connect=10.0, read=30.0, write=30.0, pool=5.0)
RETRIES = int(os.getenv("GATEWAY_RETRIES", "2"))
BATCH_SIZE = 100
MAX_UPLOAD_ROWS = 1000
FEATURE_COLUMNS = ["gender", "SeniorCitizen", "Partner", "Dependents", "tenure", "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges"]


def risk_category(probability: float) -> str:
    return "High" if probability >= 0.60 else "Medium" if probability >= 0.30 else "Low"


class CustomerCatalogue:
    """Read-only dataset with a per-process prediction cache."""

    def __init__(self, data_path: Path):
        frame = pd.read_csv(data_path)
        frame["TotalCharges"] = pd.to_numeric(frame["TotalCharges"], errors="coerce").fillna(0.0)
        self.rows = frame.to_dict(orient="records")
        self.by_id = {str(row["customerID"]): row for row in self.rows}
        self.predictions: dict[str, dict[str, Any]] = {}
        self.score_lock = asyncio.Lock()

    def payload(self, row: dict[str, Any]) -> dict[str, Any]:
        return {key: (int(row[key]) if key in {"SeniorCitizen", "tenure"} else float(row[key]) if key in {"MonthlyCharges", "TotalCharges"} else str(row[key])) for key in FEATURE_COLUMNS}

    def find(self, customer_id: str) -> dict[str, Any]:
        row = self.by_id.get(customer_id)
        if row is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        return row

    def search(self, search: str | None, contract: str | None, internet_service: str | None) -> list[dict[str, Any]]:
        query = (search or "").strip().lower()
        rows = self.rows
        if query:
            rows = [row for row in rows if query in str(row["customerID"]).lower()]
        if contract:
            rows = [row for row in rows if row["Contract"] == contract]
        if internet_service:
            rows = [row for row in rows if row["InternetService"] == internet_service]
        return rows

    def public_row(self, row: dict[str, Any]) -> dict[str, Any]:
        prediction = self.predictions.get(str(row["customerID"]))
        return {"customer_id": str(row["customerID"]), "gender": row["gender"], "tenure": int(row["tenure"]), "contract": row["Contract"], "internet_service": row["InternetService"], "monthly_charges": float(row["MonthlyCharges"]), "churn_probability": prediction["churn_probability"] if prediction else None, "prediction": prediction["prediction"] if prediction else None, "risk_category": risk_category(prediction["churn_probability"]) if prediction else None}


async def _request_json(method: str, url: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    last_error: Exception | None = None
    for _ in range(RETRIES + 1):
        try:
            response = await app.state.client.request(method, url, json=payload)
            if 400 <= response.status_code < 500:
                try:
                    detail = response.json().get("detail", response.text)
                except ValueError:
                    detail = response.text or "Upstream request was rejected"
                raise HTTPException(status_code=response.status_code, detail=detail)
            response.raise_for_status()
            try:
                return response.json()
            except ValueError as exc:
                # Render can briefly proxy an empty body while a cold service is waking.
                last_error = exc
                continue
        except (httpx.HTTPError, ValueError) as exc:
            last_error = exc
    service_name = "explanation" if "explain" in url else "prediction"
    raise HTTPException(
        status_code=502,
        detail=f"The {service_name} service is temporarily unavailable. Please retry in a moment.",
    )


async def _score_rows(rows: list[dict[str, Any]]) -> None:
    catalogue: CustomerCatalogue = app.state.catalogue
    missing = [row for row in rows if str(row["customerID"]) not in catalogue.predictions]
    if not missing:
        return
    async with catalogue.score_lock:
        missing = [row for row in missing if str(row["customerID"]) not in catalogue.predictions]
        for start in range(0, len(missing), BATCH_SIZE):
            chunk = missing[start:start + BATCH_SIZE]
            response = await _request_json("POST", f"{PREDICT_URL.rstrip('/')}/predict/batch", {"records": [catalogue.payload(row) for row in chunk]})
            for row, prediction in zip(chunk, response["results"], strict=True):
                catalogue.predictions[str(row["customerID"])] = prediction


async def _customer_with_score(row: dict[str, Any]) -> dict[str, Any]:
    await _score_rows([row])
    customer = app.state.catalogue.public_row(row)
    customer["attributes"] = app.state.catalogue.payload(row)
    return customer


@asynccontextmanager
async def lifespan(application: FastAPI):
    application.state.client = httpx.AsyncClient(timeout=TIMEOUT)
    application.state.catalogue = CustomerCatalogue(DATA_PATH)
    try:
        yield
    finally:
        await application.state.client.aclose()


app = FastAPI(title="RetentionPulse Gateway", description="Customer catalogue, prediction workflows, and model-service routing.", version="2.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=os.getenv("CORS_ORIGINS", "*").split(","), allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.exception_handler(HTTPException)
async def structured_http_error(_: Request, exc: HTTPException):
    code = "NOT_FOUND" if exc.status_code == 404 else "UPSTREAM_ERROR" if exc.status_code == 502 else "REQUEST_ERROR"
    return JSONResponse(status_code=exc.status_code, content={"error": {"code": code, "message": str(exc.detail)}})


@app.exception_handler(RequestValidationError)
async def structured_validation_error(_: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"error": {"code": "VALIDATION_ERROR", "message": "Request validation failed", "details": exc.errors()}})


@app.get("/")
@app.get("/health")
async def health():
    return {"status": "ok", "services": {"predict": PREDICT_URL, "explain": EXPLAIN_URL}, "customer_count": len(app.state.catalogue.rows)}


@app.post("/predict")
async def proxy_predict(request: Request):
    return await _request_json("POST", f"{PREDICT_URL.rstrip('/')}/predict", await request.json())


@app.post("/predict/batch")
async def proxy_batch_predict(request: Request):
    return await _request_json("POST", f"{PREDICT_URL.rstrip('/')}/predict/batch", await request.json())


@app.post("/explain")
async def proxy_explain(request: Request, top_k: int = Query(6, ge=1, le=50)):
    return await _request_json("POST", f"{EXPLAIN_URL.rstrip('/')}/explain?top_k={top_k}", await request.json())


@app.get("/dashboard")
async def dashboard():
    catalogue: CustomerCatalogue = app.state.catalogue
    probabilities = [item["churn_probability"] for item in catalogue.predictions.values()]
    return {"total_customers": len(catalogue.rows), "observed_churn_rate": sum(row["Churn"] == "Yes" for row in catalogue.rows) / len(catalogue.rows), "scored_customers": len(probabilities), "average_risk": sum(probabilities) / len(probabilities) if probabilities else None, "high_risk_customers": sum(probability >= 0.60 for probability in probabilities)}


@app.get("/customers")
async def customers(search: str | None = None, contract: str | None = None, internet_service: str | None = None, page: int = Query(1, ge=1), page_size: int = Query(25, ge=1, le=100)):
    catalogue: CustomerCatalogue = app.state.catalogue
    matches = catalogue.search(search, contract, internet_service)
    records = matches[(page - 1) * page_size:page * page_size]
    scoring_status = "available"
    try:
        await _score_rows(records)
    except HTTPException as exc:
        if exc.status_code != 429:
            raise
        # A rate-limited model service must not make the public catalogue unusable.
        scoring_status = "temporarily_unavailable"
    return {"items": [catalogue.public_row(row) for row in records], "total": len(matches), "page": page, "page_size": page_size, "scoring_status": scoring_status}


@app.get("/customers/{customer_id}")
async def customer_detail(customer_id: str):
    return await _customer_with_score(app.state.catalogue.find(customer_id))


@app.get("/customers/{customer_id}/explain")
async def customer_explanation(customer_id: str, top_k: int = Query(5, ge=1, le=10)):
    row = app.state.catalogue.find(customer_id)
    customer = await _customer_with_score(row)
    explanation = await _request_json("POST", f"{EXPLAIN_URL.rstrip('/')}/explain?top_k={top_k}", app.state.catalogue.payload(row))
    return {"customer": customer, **explanation}


@app.get("/csv-template")
async def csv_template():
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=FEATURE_COLUMNS)
    writer.writeheader()
    writer.writerows(app.state.catalogue.payload(row) for row in app.state.catalogue.rows[:10])
    return Response(buffer.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=retentionpulse-template.csv"})


@app.post("/predict/upload")
async def upload_predictions(request: Request):
    reader = csv.DictReader(io.StringIO((await request.body()).decode("utf-8-sig")))
    if not reader.fieldnames:
        raise HTTPException(status_code=422, detail="CSV must include a header row")
    missing = [column for column in FEATURE_COLUMNS if column not in reader.fieldnames]
    if missing:
        raise HTTPException(status_code=422, detail=f"CSV is missing required columns: {', '.join(missing)}")
    rows = list(reader)
    if len(rows) > MAX_UPLOAD_ROWS:
        raise HTTPException(status_code=422, detail=f"CSV exceeds the {MAX_UPLOAD_ROWS}-row limit")
    valid, errors = [], []
    for row_number, row in enumerate(rows, start=2):
        try:
            data = CustomerData.model_validate({**row, "SeniorCitizen": int(row["SeniorCitizen"]), "tenure": int(row["tenure"]), "MonthlyCharges": float(row["MonthlyCharges"]), "TotalCharges": float(row["TotalCharges"])})
            valid.append((row_number, data.model_dump()))
        except Exception as exc:
            errors.append({"row": row_number, "message": str(exc)})
    predictions = []
    for start in range(0, len(valid), BATCH_SIZE):
        chunk = valid[start:start + BATCH_SIZE]
        response = await _request_json("POST", f"{PREDICT_URL.rstrip('/')}/predict/batch", {"records": [item[1] for item in chunk]})
        predictions.extend({"row": row, **prediction} for (row, _), prediction in zip(chunk, response["results"], strict=True))
    return {"total_rows": len(rows), "successful_rows": len(predictions), "failed_rows": len(errors), "predictions": predictions, "errors": errors}
