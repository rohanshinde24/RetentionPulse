# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import pandas as pd
# import shap

# from shared.model import load_model
# from shared.schemas import CustomerData, ExplanationResponse
# from shared.utils import _normalize_df

# app = FastAPI(title="Explainability Service", version="1.0.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# model_pipeline, DECISION_THRESHOLD, MODEL_PATH = load_model()
# explainer = shap.Explainer(model_pipeline.named_steps["classifier"])

# @app.get("/")
# def health():
#     return {"status": "ok", "model_path": MODEL_PATH}

# # @app.post("/explain", response_model=ExplanationResponse)
# # def explain(data: CustomerData):
# #     df = _normalize_df(pd.DataFrame([data.dict()]))
# #     shap_values = explainer(df)

# #     contributions = []
# #     for feature_name, feature_value, shap_val in zip(df.columns, df.iloc[0].tolist(), shap_values.values[0].tolist()):
# #         contributions.append({
# #             "feature": feature_name,
# #             "value": feature_value,
# #             "shap": shap_val
# #         })

# #     explanation = {
# #         "contributions": contributions
# #     }
# #     return ExplanationResponse(explanation=explanation)
# # Define feature groups
# categorical_features = [
#     "gender",
#     "partner",
#     "dependents",
#     "phone_service",
#     "multiple_lines",
#     "internet_service",
#     "online_security",
#     "online_backup",
#     "device_protection",
#     "tech_support",
#     "streaming_tv",
#     "streaming_movies",
#     "contract",
#     "paperless_billing",
#     "payment_method"
# ]

# numerical_features = [
#     "senior_citizen",
#     "tenure",
#     "monthly_charges",
#     "total_charges"
# ]

# @app.post("/explain", response_model=ExplanationResponse)
# def explain(data: CustomerData):
#     # 1. Convert input into DataFrame
#     df = _normalize_df(pd.DataFrame([data.dict()]))

#     # 2. Compute SHAP values
#     shap_values = explainer(df)

#     # 3. Get feature names from your preprocessing pipeline
#     ohe_feature_names = model_pipeline.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(categorical_features)
#     all_feature_names = list(numerical_features) + list(ohe_feature_names)

#     # 4. Extract SHAP values for this single record
#     shap_values_for_instance = shap_values[0]

#     # 5. Build feature-level importance dictionary
#     feature_importance = sorted(
#         [
#             {
#                 "feature": feature,
#                 "value": df.iloc[0][feature],
#                 "shap_value": float(shap_val)
#             }
#             for feature, shap_val in zip(all_feature_names, shap_values_for_instance)
#         ],
#         key=lambda x: abs(x["shap_value"]),
#         reverse=True
#     )

#     # 6. Return only the top 6 to the frontend
#     return {"explanation": feature_importance[:6]}

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import pandas as pd
# import shap

# from shared.model import load_model
# from shared.schemas import CustomerData, ExplanationResponse
# from shared.utils import _normalize_df

# # ----------------------------
# # Initialize FastAPI App
# # ----------------------------
# app = FastAPI(title="Explainability Service", version="1.0.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ----------------------------
# # Load Model + Preprocessor
# # ----------------------------
# model_pipeline, DECISION_THRESHOLD, MODEL_PATH = load_model()
# classifier = model_pipeline.named_steps["classifier"]
# preprocessor = model_pipeline.named_steps["preprocessor"]

# # Build SHAP TreeExplainer for the classifier
# explainer = shap.TreeExplainer(classifier)

# # ----------------------------
# # Feature Definitions
# # ----------------------------
# categorical_features = [
#     "gender",
#     "partner",
#     "dependents",
#     "phone_service",
#     "multiple_lines",
#     "internet_service",
#     "online_security",
#     "online_backup",
#     "device_protection",
#     "tech_support",
#     "streaming_tv",
#     "streaming_movies",
#     "contract",
#     "paperless_billing",
#     "payment_method"
# ]

# numerical_features = [
#     "senior_citizen",
#     "tenure",
#     "monthly_charges",
#     "total_charges"
# ]

# # ----------------------------
# # Health Endpoint
# # ----------------------------
# @app.get("/")
# def health():
#     return {"status": "ok", "model_path": MODEL_PATH}

# # ----------------------------
# # Explain Endpoint
# # ----------------------------
# @app.post("/explain", response_model=ExplanationResponse)
# def explain(data: CustomerData):
#     # 1. Convert input into DataFrame
#     df = _normalize_df(pd.DataFrame([data.dict()]))

#     # 2. Apply preprocessing (transform into numeric form)
#     df_transformed = preprocessor.transform(df)

#     # 3. Get feature names after encoding
#     ohe_encoder = preprocessor.named_transformers_['cat']
#     ohe_feature_names = ohe_encoder.get_feature_names_out(ohe_encoder.feature_names_in_)
#     all_feature_names = list(numerical_features) + list(ohe_feature_names)

#     # 4. Compute SHAP values on transformed data
#     shap_values = explainer(df_transformed)

#     # 5. Extract SHAP values for the first record
#     shap_values_for_instance = shap_values[0]

#     # 6. Build feature-level importance dictionary
#     feature_importance = sorted(
#         [
#             {
#                 "feature": feature,
#                 "value": df_transformed[0][id],  # use transformed value
#                 "shap_value": float(shap_val)
#             }
#             for feature, shap_val in zip(all_feature_names, shap_values_for_instance.values)
#         ],
#         key=lambda x: abs(x["shap_value"]),
#         reverse=True
#     )

#     # 7. Return top 6 features
#     return {"explanation": feature_importance[:6]}
# api/explain_service/main.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
import shap

from shared.model import load_model
from shared.schemas import CustomerData
from shared.utils import _normalize_df

app = FastAPI(title="Explainability Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model + pull out components
model_pipeline, DECISION_THRESHOLD, MODEL_PATH = load_model()
preprocessor = model_pipeline.named_steps["preprocessor"]
classifier = model_pipeline.named_steps["classifier"]

# SHAP explainer for the trained LightGBM classifier
explainer = shap.TreeExplainer(classifier)

@app.get("/")
def health():
    return {"status": "ok", "model_path": MODEL_PATH}

@app.post("/explain")
def explain(data: CustomerData, top_k: int = Query(6, ge=1, le=50)):
    """
    Returns top-k SHAP feature contributions for a single row, matching frontend shape:
    {
      "top_features": [
        {"name": "...", "abs_shap": float, "shap": float},
        ...
      ]
    }
    """
    # 1) Build a DataFrame with EXACT training column names & types
    #    _normalize_df should map your snake_case payload to the training schema
    X_raw = _normalize_df(pd.DataFrame([data.dict()]))

    # 2) Transform with the fitted preprocessor (OHE + scaling)
    X_t = preprocessor.transform(X_raw)

    # Convert to dense row vector for easy indexing
    if hasattr(X_t, "toarray"):
        row = X_t[0].toarray().ravel()
    else:
        row = np.asarray(X_t[0]).ravel()

    # 3) Reconstruct transformed feature names in the SAME order as X_t columns
    #    Get the original numeric/categorical column lists from the fitted preprocessor
    num_cols = []
    cat_cols = []
    for name, _, cols in preprocessor.transformers_:
        if name == "num":
            num_cols = list(cols) if isinstance(cols, (list, tuple, pd.Index)) else []
        elif name == "cat":
            cat_cols = list(cols) if isinstance(cols, (list, tuple, pd.Index)) else []

    # OneHotEncoder expanded names (use learned names to avoid mismatch errors)
    ohe = preprocessor.named_transformers_["cat"]
    # Using learned feature names (no args) avoids "input_features is not equal to feature_names_in_"
    ohe_feature_names = list(ohe.get_feature_names_out())

    all_feature_names = list(num_cols) + ohe_feature_names

    # 4) Compute SHAP values on the transformed matrix
    sv = explainer(X_t)  # Explanation object

    # Take this single row’s contributions; handle multiclass shape if present
    values = sv.values
    if values.ndim == 3:  # e.g., (n_samples, n_features, n_classes)
        values = values[:, :, 1]  # positive class

    shap_row = values[0]  # 1D array of length n_features

    # 5) Zip names with shap values (and optionally transformed value if needed)
    #    Your frontend expects: { name, abs_shap, shap }
    pairs = []
    for i, (fname, s) in enumerate(zip(all_feature_names, shap_row)):
        # transformed feature value is row[i] if you ever want to return it
        pairs.append(
            {"name": str(fname), "abs_shap": float(abs(s)), "shap": float(s)}
        )

    # 6) Sort by absolute contribution and return top-k
    pairs.sort(key=lambda x: x["abs_shap"], reverse=True)
    return {"top_features": pairs[:top_k]}
