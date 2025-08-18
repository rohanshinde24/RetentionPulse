import pandas as pd

_expected_input_columns = [
    "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
    "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity",
    "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
    "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod",
    "MonthlyCharges", "TotalCharges"
]

def _normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure DataFrame has the expected columns and correct order"""
    df = df.copy()
    df.columns = [c.strip().replace(" ", "") for c in df.columns]  # keep casing
    for col in _expected_input_columns:
        if col not in df.columns:
            df[col] = 0
    return df[_expected_input_columns]
