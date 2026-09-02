from fastapi.testclient import TestClient
from prediction_service.main import app
from tests.conftest import sample_payload

client = TestClient(app)


def test_health_endpoint():
    assert client.get("/").json()["status"] == "ok"


def test_predict_single_returns_model_contract():
    response = client.post("/predict", json=sample_payload())
    assert response.status_code == 200
    body = response.json()
    assert body["prediction"] in {"Churn", "No Churn"}
    assert 0 <= body["churn_probability"] <= 1
    assert body["threshold"] == 0.5


def test_predict_batch_is_bounded():
    assert client.post("/predict/batch", json={"records": [sample_payload()] * 101}).status_code == 422


def test_predict_requires_all_customer_fields():
    payload = sample_payload()
    payload.pop("MonthlyCharges")
    assert client.post("/predict", json=payload).status_code == 422
