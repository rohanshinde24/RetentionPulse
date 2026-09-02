from fastapi import HTTPException
from fastapi.testclient import TestClient
from gateway_service import main as gateway
from tests.conftest import sample_payload


async def fake_request(_: str, url: str, payload=None):
    if "explain" in url:
        return {"top_features": [{"name": "Contract_Month-to-month", "abs_shap": 0.4, "shap": 0.4}]}
    records = payload["records"] if "records" in payload else [payload]
    return {"results": [{"prediction": "Churn", "churn_probability": 0.71, "threshold": 0.5} for _ in records]}


def test_gateway_catalogue_and_upload_contract(monkeypatch):
    monkeypatch.setattr(gateway, "_request_json", fake_request)
    with TestClient(gateway.app) as client:
        assert client.get("/health").json()["customer_count"] == 7043
        customers = client.get("/customers?page_size=2")
        assert len(customers.json()["items"]) == 2
        assert customers.json()["items"][0]["risk_category"] == "High"
        assert client.get("/customers/7590-VHVEG/explain").json()["top_features"][0]["name"] == "Contract_Month-to-month"
        template = client.get("/csv-template").text
        assert "MonthlyCharges" in template
        assert len(template.strip().splitlines()) == 11
        header = ",".join(gateway.FEATURE_COLUMNS)
        row = ",".join(str(sample_payload()[column]) for column in gateway.FEATURE_COLUMNS)
        upload = client.post("/predict/upload", content=f"{header}\n{row}\n", headers={"Content-Type": "text/csv"})
        assert upload.status_code == 200
        assert upload.json()["successful_rows"] == 1


def test_gateway_rejects_csv_without_required_columns(monkeypatch):
    monkeypatch.setattr(gateway, "_request_json", fake_request)
    with TestClient(gateway.app) as client:
        response = client.post("/predict/upload", content="tenure\n12\n", headers={"Content-Type": "text/csv"})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "REQUEST_ERROR"


def test_gateway_keeps_catalogue_available_when_model_is_rate_limited(monkeypatch):
    async def rate_limited_request(_: str, __: str, payload=None):
        raise HTTPException(status_code=429, detail="Too Many Requests")

    monkeypatch.setattr(gateway, "_request_json", rate_limited_request)
    with TestClient(gateway.app) as client:
        response = client.get("/customers?page_size=2")

    assert response.status_code == 200
    assert len(response.json()["items"]) == 2
    assert response.json()["scoring_status"] == "temporarily_unavailable"
