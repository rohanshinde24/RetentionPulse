import pytest
from fastapi.testclient import TestClient
from main_predict import app   # prediction service

client = TestClient(app)

def sample_payload():
    return {
        "gender": "Male",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "No",
        "tenure": 24,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "DSL",
        "OnlineSecurity": "Yes",
        "OnlineBackup": "Yes",
        "DeviceProtection": "No",
        "TechSupport": "Yes",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "One year",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Mailed check",
        "MonthlyCharges": 59.9,
        "TotalCharges": 1400.0,
    }

def test_health_endpoint():
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert "status" in body
    assert body["status"] in {"ok", "error"}

def test_predict_single_smoke():
    r = client.post("/predict", json=sample_payload())
    assert r.status_code == 200
    body = r.json()
    assert "prediction" in body
    assert "churn_probability" in body
    assert "threshold" in body

def test_predict_batch_smoke():
    payload = {"records": [sample_payload(), sample_payload()]}
    r = client.post("/predict/batch", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "results" in body
    assert isinstance(body["results"], list)
    assert len(body["results"]) == 2
    for item in body["results"]:
        assert "prediction" in item
        assert "churn_probability" in item
        assert "threshold" in item

def test_validation_missing_field():
    bad = sample_payload()
    bad.pop("MonthlyCharges")
    r = client.post("/predict", json=bad)
    assert r.status_code == 422
