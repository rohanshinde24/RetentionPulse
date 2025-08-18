import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "model.pkl")
DECISION_THRESHOLD = 0.5

def load_model():
    model_pipeline = joblib.load(MODEL_PATH)
    return model_pipeline, DECISION_THRESHOLD, MODEL_PATH
