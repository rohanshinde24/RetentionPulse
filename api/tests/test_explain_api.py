from fastapi.testclient import TestClient
from explain_service.main import app
from tests.conftest import sample_payload

client = TestClient(app)


def test_explain_returns_ordered_feature_contract():
    response = client.post("/explain?top_k=5", json=sample_payload())
    assert response.status_code == 200
    features = response.json()["top_features"]
    assert len(features) == 5
    assert all({"name", "abs_shap", "shap"} <= feature.keys() for feature in features)
    assert features == sorted(features, key=lambda feature: feature["abs_shap"], reverse=True)
    assert isinstance(response.json()["other_shap"], float)
    assert 0 <= response.json()["base_probability"] <= 1
    assert 0 <= response.json()["output_probability"] <= 1
