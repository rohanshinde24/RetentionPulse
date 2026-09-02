"""Shared model loading configuration."""
import os
from pathlib import Path

import joblib

DEFAULT_MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "model.pkl"
DECISION_THRESHOLD = float(os.getenv("DECISION_THRESHOLD", "0.5"))


def load_model():
    model_path = Path(os.getenv("MODEL_PATH", str(DEFAULT_MODEL_PATH)))
    return joblib.load(model_path), DECISION_THRESHOLD, str(model_path)
