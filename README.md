# RetentionPulse — An Interpretable Churn Prediction System

**RetentionPulse** is an end-to-end machine learning system that predicts customer churn for a subscription business and explains **why** a prediction was made using SHAP. It’s built as a small set of FastAPI microservices behind a gateway, with a React + Vite TypeScript UI.

## ✨ Highlights

- **Model**: LightGBM (scikit-learn pipeline) serialized with `joblib`
- **Interpretability**: SHAP feature attributions for each prediction
- **APIs**: FastAPI microservices (prediction + explain) behind a gateway
- **Frontend**: React + Vite (TypeScript), Tailwind
- **Deployability**: Works locally and on Render (three backend services + static UI)

---

## 🧱 Repository Structure

```
RetentionPulse/
├── api/
│   ├── prediction_service/
│   │   └── main.py              # /predict and health
│   ├── explain_service/
│   │   └── main.py              # /explain and health (SHAP)
│   ├── gateway_service/
│   │   └── main.py              # routes /predict and /explain to services
│   ├── shared/
│   │   ├── model.py             # load_model() & env handling
│   │   ├── schemas.py           # Pydantic models (request/response)
│   │   └── utils.py             # normalization / alignment helpers
│   ├── models/
│   │   └── model.pkl            # LightGBM pipeline (commit for simple deploy)
│   ├── requirements.txt
│   └── runtime.txt              # (optional) python-3.11.x for Render
├── ui/
│   └── retentionpulse-ui/       # Vite + React (TS) app
│       ├── src/
│       ├── index.html
│       ├── package.json
│       └── .env.local           # VITE_API_BASE for local dev
├── data/                        # (optional) datasets (not needed for serving)
├── notebooks/                   # (optional) model dev notebooks
└── README.md
```

---

## 📊 Model Performance

Evaluated on a held-out test set:

- **ROC AUC**: **0.84**

This indicates strong separation between churners vs. non-churners.

**Top churn drivers (SHAP):** contract type, tenure, and internet service, among others. The Explain API returns the top feature contributions per customer.

---

## 🚀 Quick Start (Local Development)

> **Prereqs:** Python 3.11 recommended (SHAP/LightGBM friendly), Node 18+ / 20+ for the UI.

### 1) Create & activate a Python venv, install deps

```bash
cd RetentionPulse
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

cd api
pip install -r requirements.txt
```

> Ensure the model file exists at `api/models/model.pkl`.
> You can override the path via `MODEL_PATH` env var.

### 2) Run microservices (3 terminals)

**Terminal A — prediction service (port 8001):**

```bash
cd RetentionPulse
source venv/bin/activate
cd api
export MODEL_PATH=models/model.pkl
python -m uvicorn prediction_service.main:app --reload --port 8001
```

**Terminal B — explain service (port 8002):**

```bash
cd RetentionPulse
source venv/bin/activate
cd api
export MODEL_PATH=models/model.pkl
python -m uvicorn explain_service.main:app --reload --port 8002
```

**Terminal C — gateway service (port 8000):**

```bash
cd RetentionPulse
source venv/bin/activate
cd api
export PREDICT_URL=http://localhost:8001
export EXPLAIN_URL=http://localhost:8002
python -m uvicorn gateway_service.main:app --reload --port 8000
```

Gateway health: [http://localhost:8000/](http://localhost:8000/)

### 3) Start the UI (port 5173)

```bash
cd RetentionPulse/ui/retentionpulse-ui
# Set the gateway for local dev:
echo "VITE_API_BASE=http://localhost:8000" > .env.local

npm install
npm run dev
```

Open: [http://localhost:5173](http://localhost:5173)

You should see the app, with API health showing **ok**, and be able to **Predict** and **Explain**.

---

## 🧪 API Endpoints

All calls should go through the **gateway** in dev/prod:

- **Gateway base**: `http://localhost:8000`

### Predict

`POST /predict`

**Request body** (fields match the training schema):

```json
{
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
  "TotalCharges": 1400.0
}
```

**Response:**

```json
{
  "prediction": "Churn",
  "churn_probability": 0.63,
  "threshold": 0.5
}
```

### Explain

`POST /explain?top_k=6` (top_k optional)

**Request body**: same as `/predict`.

**Response:**

```json
{
  "top_features": [
    { "name": "Contract_Two year", "abs_shap": 0.42, "shap": -0.42 },
    { "name": "tenure", "abs_shap": 0.25, "shap": -0.25 },
    ...
  ]
}
```

### Health

- **Gateway**: `GET /` → `{ status: "ok", services: {...} }`
- **Prediction service**: `GET /` → `{ status: "ok", model_path: "..." }`
- **Explain service**: `GET /` → `{ status: "ok", model_path: "..." }`

---

## ⚙️ Configuration

**Environment variables (backend):**

- `MODEL_PATH` — path to the serialized model (default: `models/model.pkl` when running from `api/`)
- `DECISION_THRESHOLD` — optional, default `0.5`
- `PREDICT_URL` (gateway) — URL of prediction service (default: `http://localhost:8001`)
- `EXPLAIN_URL` (gateway) — URL of explain service (default: `http://localhost:8002`)

**Frontend:**

- `ui/retentionpulse-ui/.env.local`

  ```
  VITE_API_BASE=http://localhost:8000
  ```

---

## ✅ Testing

Backend tests (smoke tests live under `api/tests`):

```bash
cd RetentionPulse
source venv/bin/activate
cd api
pytest -q
```

---

## ☁️ Deployment (Render)

Create **three Web Services** for the backend (all pointing to the same repo, root dir = `api`) and **one Static Site** for the UI.

1. **prediction_service**

- Build: `pip install -r requirements.txt`
- Start: `uvicorn prediction_service.main:app --host 0.0.0.0 --port $PORT`
- Env: `MODEL_PATH=models/model.pkl`

2. **explain_service**

- Build: `pip install -r requirements.txt`
- Start: `uvicorn explain_service.main:app --host 0.0.0.0 --port $PORT`
- Env: `MODEL_PATH=models/model.pkl`

3. **gateway_service**

- Build: `pip install -r requirements.txt`
- Start: `uvicorn gateway_service.main:app --host 0.0.0.0 --port $PORT`
- Env:

  - `PREDICT_URL=https://<your-prediction-service>.onrender.com`
  - `EXPLAIN_URL=https://<your-explain-service>.onrender.com`

4. **Frontend (Static Site)**

- Root Directory: `ui/retentionpulse-ui`
- Build: `npm ci && npm run build`
- Publish dir: `dist`
- Env:

  - `VITE_API_BASE=https://<your-gateway-service>.onrender.com`

> **CORS:** Add your frontend URL to the gateway CORS `allow_origins` list.

---

## 🔍 Notes & Tips

- **Model file**: easiest path is to commit `api/models/model.pkl`. For larger models, use object storage and set `MODEL_PATH` to a downloaded path at startup.
- **Python version**: Prefer **3.11** for SHAP + LightGBM compatibility (add `api/runtime.txt` with `python-3.11.9` on Render).
- **Feature schema**: The APIs expect the same feature names used to train the pipeline (as in the sample JSON above). The backend normalizes/aligns inputs before scoring and explaining.
- **Threshold tuning**: Set `DECISION_THRESHOLD` per your business tolerance for recall vs. precision.
