RetentionPulse – An Interpretable Churn Prediction System
Objective
This project is an end-to-end machine learning system designed to predict customer churn for a subscription-based service, directly addressing a key business challenge mentioned in the Adobe ML Internship job description.

The system uses a high-performance LightGBM model and provides interpretable insights using SHAP (SHapley Additive exPlanations) to explain the key drivers behind churn. The final model is deployed as a lightweight REST API using FastAPI for easy integration into production systems.

Tech Stack
Python 3.9+

Modeling: scikit-learn, LightGBM

Data Handling: pandas

Interpretability: SHAP

API Deployment: FastAPI, Uvicorn

Model Serialization: joblib

Model Performance
The model was evaluated on a held-out test set and achieved the following performance:

ROC AUC Score: 0.84

This score indicates a strong ability to distinguish between customers who will churn and those who will not.

Key Churn Drivers (Model Interpretability)
To ensure the model is not a "black box," SHAP was used to identify the most influential features driving churn predictions. The summary plot below shows that factors like contract type, tenure, and internet service are the most significant predictors.

How to Run the System Locally

1. Clone the Repository

git clone https://github.com/<YOUR_USERNAME>/RetentionPulse.git
cd RetentionPulse

2. Set Up a Virtual Environment and Install Dependencies

# Create and activate a virtual environment

python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`

# Install required packages

pip install -r requirements.txt

3. Run the Prediction API

Once the dependencies are installed, you can start the API server using Uvicorn.

uvicorn main:app --reload

The API will be available at http://127.0.0.1:8000.

4. Access the Interactive API Documentation

You can interact with the API and send test requests by navigating to the auto-generated Swagger UI documentation in your browser:

http://127.0.0.1:8000/docs
