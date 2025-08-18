# # main.py

# # --- 1. Imports ---
# import uvicorn
# import joblib
# import pandas as pd
# from fastapi import FastAPI
# from pydantic import BaseModel

# # --- 2. Initialize FastAPI app ---
# app = FastAPI(
#     title="RetentionPulse API",
#     description="An API for predicting customer churn using a LightGBM model.",
#     version="1.0.0"
# )

# # --- 3. Load the Model Pipeline ---
# # Load the entire pipeline object you saved from the notebook
# try:
#     model_pipeline = joblib.load('retention_pulse_pipeline.pkl')
#     print("Model pipeline loaded successfully.")
# except FileNotFoundError:
#     print("Error: Model file 'retention_pulse_pipeline.pkl' not found.")
#     model_pipeline = None
# except Exception as e:
#     print(f"An error occurred while loading the model: {e}")
#     model_pipeline = None

# # --- 4. Define the Input Data Model using Pydantic ---
# # This ensures that the incoming data has the correct structure and types.
# # These fields MUST match the column names of the data used for training.
# class CustomerData(BaseModel):
#     gender: str
#     SeniorCitizen: int
#     Partner: str
#     Dependents: str
#     tenure: int
#     PhoneService: str
#     MultipleLines: str
#     InternetService: str
#     OnlineSecurity: str
#     OnlineBackup: str
#     DeviceProtection: str
#     TechSupport: str
#     StreamingTV: str
#     StreamingMovies: str
#     Contract: str
#     PaperlessBilling: str
#     PaymentMethod: str
#     MonthlyCharges: float
#     TotalCharges: float

#     class Config:
#         # Provide an example for the API documentation (Swagger UI)
#         schema_extra = {
#             "example": {
#                 "gender": "Male",
#                 "SeniorCitizen": 0,
#                 "Partner": "Yes",
#                 "Dependents": "No",
#                 "tenure": 24,
#                 "PhoneService": "Yes",
#                 "MultipleLines": "No",
#                 "InternetService": "DSL",
#                 "OnlineSecurity": "Yes",
#                 "OnlineBackup": "Yes",
#                 "DeviceProtection": "No",
#                 "TechSupport": "Yes",
#                 "StreamingTV": "No",
#                 "StreamingMovies": "No",
#                 "Contract": "One year",
#                 "PaperlessBilling": "Yes",
#                 "PaymentMethod": "Mailed check",
#                 "MonthlyCharges": 59.9,
#                 "TotalCharges": 1400.0
#             }
#         }


# # --- 5. Define the Prediction Endpoint ---
# @app.post("/predict")
# def predict_churn(data: CustomerData):
#     """
#     Predicts the probability of churn for a single customer.

#     - **data**: A JSON object containing customer features.

#     Returns:
#     - A JSON object with the churn prediction and probability.
#     """
#     if not model_pipeline:
#         return {"error": "Model is not loaded. Cannot make predictions."}

#     # Convert the incoming Pydantic model to a pandas DataFrame
#     # The model pipeline expects a DataFrame as input
#     input_df = pd.DataFrame([data.dict()])

#     # Use the pipeline to get the prediction probability
#     # `predict_proba` returns probabilities for both classes [class_0, class_1]
#     # We want the probability of churn (class 1)
#     churn_probability = model_pipeline.predict_proba(input_df)[0][1]

#     # Determine the prediction based on a 0.5 threshold
#     prediction = "Churn" if churn_probability > 0.5 else "No Churn"

#     return {
#         "prediction": prediction,
#         "churn_probability": float(churn_probability)
#     }

# # --- 6. Define a Root Endpoint for Health Check ---
# @app.get("/")
# def read_root():
#     return {"status": "ok", "message": "Welcome to the RetentionPulse Churn Prediction API!"}


# # --- 7. Main block to run the app ---
# # This allows you to run the API directly with `python main.py`
# # For production, it's better to use Uvicorn directly from the command line.
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

"""
RetentionPulse API
------------------
FastAPI service for customer churn prediction with:
- Single & batch scoring
- Configurable decision threshold via env
- SHAP-based top-k explanations
- Health endpoint exposing expected input schema

Run:
  MODEL_PATH=retention_pulse_pipeline.pkl DECISION_THRESHOLD=0.50 uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
"""

# # --- 1) Imports ---
# import os
# from enum import Enum
# from typing import List, Optional

# import joblib
# import numpy as np
# import pandas as pd
# import uvicorn
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel, Field


# # --- 2) App & Config ---
# app = FastAPI(
#     title="RetentionPulse API",
#     description="An API for predicting customer churn using a LightGBM model.",
#     version="1.1.0",
# )

# # Allow calling from a local dashboard or other frontends (optional; tighten for prod)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# MODEL_PATH = os.getenv("MODEL_PATH", "models/retention_pulse_pipeline.pkl")
# try:
#     DECISION_THRESHOLD = float(os.getenv("DECISION_THRESHOLD", "0.50"))
# except ValueError:
#     DECISION_THRESHOLD = 0.50


# # --- 3) Load Model Pipeline ---
# model_pipeline = None
# try:
#     model_pipeline = joblib.load(MODEL_PATH)
#     print(f"[RetentionPulse] Model pipeline loaded from {MODEL_PATH}")
# except FileNotFoundError:
#     print(f"[RetentionPulse] ERROR: Model file '{MODEL_PATH}' not found.")
# except Exception as e:
#     print(f"[RetentionPulse] ERROR loading model: {e}")


# # --- 4) Schemas (with lightweight validation) ---
# class YesNo(str, Enum):
#     Yes = "Yes"
#     No = "No"


# class ContractType(str, Enum):
#     month_to_month = "Month-to-month"
#     one_year = "One year"
#     two_year = "Two year"


# class InternetServiceType(str, Enum):
#     dsl = "DSL"
#     fiber = "Fiber optic"
#     none = "No"


# class CustomerData(BaseModel):
#     # Matches Telco Churn raw columns used during training
#     gender: str
#     SeniorCitizen: int = Field(ge=0, le=1)
#     Partner: YesNo
#     Dependents: YesNo
#     tenure: int = Field(ge=0)
#     PhoneService: YesNo
#     MultipleLines: str  # can be "No phone service"
#     InternetService: InternetServiceType
#     OnlineSecurity: str  # can be "No internet service"
#     OnlineBackup: str
#     DeviceProtection: str
#     TechSupport: str
#     StreamingTV: str
#     StreamingMovies: str
#     Contract: ContractType
#     PaperlessBilling: YesNo
#     PaymentMethod: str
#     MonthlyCharges: float
#     TotalCharges: float

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "gender": "Male",
#                 "SeniorCitizen": 0,
#                 "Partner": "Yes",
#                 "Dependents": "No",
#                 "tenure": 24,
#                 "PhoneService": "Yes",
#                 "MultipleLines": "No",
#                 "InternetService": "DSL",
#                 "OnlineSecurity": "Yes",
#                 "OnlineBackup": "Yes",
#                 "DeviceProtection": "No",
#                 "TechSupport": "Yes",
#                 "StreamingTV": "No",
#                 "StreamingMovies": "No",
#                 "Contract": "One year",
#                 "PaperlessBilling": "Yes",
#                 "PaymentMethod": "Mailed check",
#                 "MonthlyCharges": 59.9,
#                 "TotalCharges": 1400.0,
#             }
#         }


# class PredictionResponse(BaseModel):
#     prediction: str
#     churn_probability: float
#     threshold: float


# class BatchRequest(BaseModel):
#     records: List[CustomerData]


# class BatchPredictionResponse(BaseModel):
#     results: List[PredictionResponse]


# # --- 5) Helpers ---
# def _normalize_df(df: pd.DataFrame) -> pd.DataFrame:
#     """Normalize strings and avoid surprises in OHE/string matching."""
#     df = df.copy()
#     for c in df.columns:
#         if df[c].dtype == object:
#             df[c] = df[c].astype(str).str.strip()
#     return df


# def _expected_input_columns() -> Optional[List[str]]:
#     """Return the raw input column names the preprocessor expects, if available."""
#     if not model_pipeline:
#         return None
#     try:
#         pre = model_pipeline.named_steps["preprocessor"]
#         cols: List[str] = []
#         # pre.transformers_ is a list of tuples: (name, transformer, column_list)
#         for _, _, col_list in pre.transformers_:
#             if isinstance(col_list, list):
#                 cols.extend(col_list)
#         return cols
#     except Exception:
#         return None


# # --- 6) Endpoints ---
# @app.get("/", tags=["health"])
# def health():
#     """Basic health with schema hint (useful for clients)."""
#     status = "ok" if model_pipeline is not None else "error"
#     return {
#         "status": status,
#         "message": "RetentionPulse API",
#         "model_path": MODEL_PATH,
#         "decision_threshold": DECISION_THRESHOLD,
#         "expected_input_columns": _expected_input_columns(),
#     }


# @app.post("/predict", response_model=PredictionResponse, tags=["predict"])
# def predict_churn(data: CustomerData):
#     """Score a single customer."""
#     if not model_pipeline:
#         return PredictionResponse(
#             prediction="error",
#             churn_probability=0.0,
#             threshold=DECISION_THRESHOLD,
#         )

#     input_df = _normalize_df(pd.DataFrame([data.dict()]))
#     prob = float(model_pipeline.predict_proba(input_df)[0][1])
#     label = "Churn" if prob >= DECISION_THRESHOLD else "No Churn"
#     return PredictionResponse(
#         prediction=label,
#         churn_probability=prob,
#         threshold=DECISION_THRESHOLD,
#     )


# @app.post("/predict/batch", response_model=BatchPredictionResponse, tags=["predict"])
# def predict_batch(payload: BatchRequest):
#     """Score a batch of customers."""
#     if not model_pipeline:
#         return BatchPredictionResponse(results=[])

#     df = _normalize_df(pd.DataFrame([r.dict() for r in payload.records]))
#     probs = model_pipeline.predict_proba(df)[:, 1]
#     results: List[PredictionResponse] = []
#     for p in probs:
#         label = "Churn" if float(p) >= DECISION_THRESHOLD else "No Churn"
#         results.append(
#             PredictionResponse(
#                 prediction=label,
#                 churn_probability=float(p),
#                 threshold=DECISION_THRESHOLD,
#             )
#         )
#     return BatchPredictionResponse(results=results)


# @app.post("/explain", tags=["explain"])
# def explain_row(data: CustomerData, top_k: int = 5):
#     """
#     Return top-k SHAP feature contributions for a single row.
#     (TreeExplainer over LightGBM; uses transformed feature matrix.)
#     """
#     if not model_pipeline:
#         return {"error": "Model not loaded"}

#     try:
#         import shap  # imported here to keep base runtime light

#         # Transform input
#         X_raw = _normalize_df(pd.DataFrame([data.dict()]))
#         pre = model_pipeline.named_steps["preprocessor"]
#         X_t = pre.transform(X_raw)

#         # Model
#         clf = model_pipeline.named_steps["classifier"]
#         explainer = shap.TreeExplainer(clf)
#         sv = explainer(X_t)

#         values = sv.values
#         # If multiclass, take class 1 contributions
#         if values.ndim == 3:
#             values = values[:, :, 1]
#         contrib = values[0]

#         # Reconstruct feature names: [num_cols] + OHE(cat_cols)
#         num_cols = []
#         cat_cols = []
#         try:
#             for name, _, cols in pre.transformers_:
#                 if name == "num":
#                     num_cols = list(cols) if isinstance(cols, list) else []
#                 elif name == "cat":
#                     cat_cols = list(cols) if isinstance(cols, list) else []
#         except Exception:
#             pass

#         try:
#             ohe_names = pre.named_transformers_["cat"].get_feature_names_out(cat_cols)
#         except Exception:
#             # fallback if names not available
#             ohe_names = [f"{c}_encoded" for c in cat_cols]

#         feat_names = list(num_cols) + list(ohe_names)

#         # Guard length mismatch
#         if len(feat_names) != len(contrib):
#             feat_names = [f"f{i}" for i in range(len(contrib))]

#         pairs = sorted(
#             zip(feat_names, np.abs(contrib), contrib),
#             key=lambda x: x[1],
#             reverse=True,
#         )[: max(1, int(top_k))]

#         return {
#             "top_features": [
#                 {"name": n, "abs_shap": float(a), "shap": float(s)} for n, a, s in pairs
#             ]
#         }

#     except Exception as e:
#         return {"error": f"explain failed: {e}"}


# # --- 7) Main (dev convenience) ---
# if __name__ == "__main__":
#     # For production, prefer: `uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2`
#     uvicorn.run(app, host="0.0.0.0", port=8000, workers=2)
