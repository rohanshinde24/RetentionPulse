# from pydantic import BaseModel
# from typing import List

# class CustomerData(BaseModel):
#     gender: str
#     senior_citizen: int
#     partner: str
#     dependents: str
#     tenure: int
#     phone_service: str
#     multiple_lines: str
#     internet_service: str
#     online_security: str
#     online_backup: str
#     device_protection: str
#     tech_support: str
#     streaming_tv: str
#     streaming_movies: str
#     contract: str
#     paperless_billing: str
#     payment_method: str
#     monthly_charges: float
#     total_charges: float


# class PredictionResponse(BaseModel):
#     prediction: str
#     churn_probability: float
#     threshold: float

# class BatchRequest(BaseModel):
#     records: List[CustomerData]

# class BatchPredictionResponse(BaseModel):
#     results: List[PredictionResponse]

# class ExplanationResponse(BaseModel):
#     explanation: dict
from enum import Enum
from typing import List
from pydantic import BaseModel, Field


# --- Enums for categorical features ---
class YesNo(str, Enum):
    Yes = "Yes"
    No = "No"


class ContractType(str, Enum):
    month_to_month = "Month-to-month"
    one_year = "One year"
    two_year = "Two year"


class InternetServiceType(str, Enum):
    dsl = "DSL"
    fiber = "Fiber optic"
    none = "No"


# --- Main Schema ---
class CustomerData(BaseModel):
    # Matches training data columns
    gender: str
    SeniorCitizen: int = Field(ge=0, le=1)
    Partner: YesNo
    Dependents: YesNo
    tenure: int = Field(ge=0)
    PhoneService: YesNo
    MultipleLines: str  # can be "No phone service"
    InternetService: InternetServiceType
    OnlineSecurity: str  # can be "No internet service"
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: ContractType
    PaperlessBilling: YesNo
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

    class Config:
        json_schema_extra = {
            "example": {
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
        }


# --- Response Schemas ---
class PredictionResponse(BaseModel):
    prediction: str
    churn_probability: float
    threshold: float


class BatchRequest(BaseModel):
    records: List[CustomerData]


class BatchPredictionResponse(BaseModel):
    results: List[PredictionResponse]


class ExplanationResponse(BaseModel):
    explanation: dict
# class ExplanationResponse(BaseModel):
#     explanation: dict  # or refine into List[dict]
