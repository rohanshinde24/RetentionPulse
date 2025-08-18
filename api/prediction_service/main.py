from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from shared.model import load_model
from shared.schemas import CustomerData, PredictionResponse, BatchRequest, BatchPredictionResponse
from shared.utils import _normalize_df

app = FastAPI(title="Prediction Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_pipeline, DECISION_THRESHOLD, MODEL_PATH = load_model()

@app.get("/")
def health():
    status = "ok" if model_pipeline else "error"
    return {"status": status, "model_path": MODEL_PATH}

@app.post("/predict", response_model=PredictionResponse)
def predict_churn(data: CustomerData):
    df = _normalize_df(pd.DataFrame([data.dict()]))
    prob = float(model_pipeline.predict_proba(df)[0][1])
    label = "Churn" if prob >= DECISION_THRESHOLD else "No Churn"
    return PredictionResponse(prediction=label, churn_probability=prob, threshold=DECISION_THRESHOLD)

@app.post("/predict/batch", response_model=BatchPredictionResponse)
def predict_batch(payload: BatchRequest):
    df = _normalize_df(pd.DataFrame([r.dict() for r in payload.records]))
    probs = model_pipeline.predict_proba(df)[:, 1]
    results = []
    for p in probs:
        label = "Churn" if float(p) >= DECISION_THRESHOLD else "No Churn"
        results.append(PredictionResponse(prediction=label, churn_probability=float(p), threshold=DECISION_THRESHOLD))
    return BatchPredictionResponse(results=results)
