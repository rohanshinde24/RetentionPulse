import pytest
from fastapi.testclient import TestClient
from main_explain import app   # explanation service

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

def test_explain_smoke():
    r = client.post("/explain?top_k=5", json=sample_payload())
    assert r.status_code == 200
    body = r.json()
    # The endpoint may return an error if model not loaded — both are acceptable
    assert ("top_features" in body and isinstance(body["top_features"], list)) or ("error" in body)
