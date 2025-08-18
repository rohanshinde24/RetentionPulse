# from fastapi import FastAPI, Request
# import httpx
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse



# app = FastAPI(
#     title="RetentionPulse Gateway",
#     description="Gateway service that routes to predict and explain microservices",
#     version="1.0.0",
# )

# # Allow frontend (Vite/React) to call the gateway
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # ["*"] or restrict to ["http://localhost:5173"] if your frontend runs there
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# # @app.options("/{full_path:path}")
# # async def preflight_handler(full_path: str):
# #     return JSONResponse(content={"message": "OK"})
# # Microservice base URLs
# PREDICT_URL = "http://localhost:8001"
# EXPLAIN_URL = "http://localhost:8002"

# client = httpx.AsyncClient()

# @app.get("/")
# async def root():
#     return {"status": "ok", "services": {"predict": PREDICT_URL, "explain": EXPLAIN_URL}}

# # @app.get("/")
# # def root():
# #     return {"message": "RetentionPulse Gateway up"}


# # @app.post("/predict")
# # async def predict(request: Request):
# #     payload = await request.json()
# #     r = await client.post(f"{PREDICT_URL}/predict", json=payload)
# #     return r.json()


# # @app.post("/explain")
# # async def explain(request: Request):
# #     payload = await request.json()
# #     r = await client.post(f"{EXPLAIN_URL}/explain", json=payload)
# #     return r.json()
# @app.post("/predict")
# async def proxy_predict(request: Request):
#     data = await request.json()
#     async with httpx.AsyncClient() as client:
#         resp = await client.post(f"{PREDICT_URL}/predict", json=data)
#     return resp.json()

# @app.post("/explain")
# async def proxy_explain(request: Request):
#     data = await request.json()
#     async with httpx.AsyncClient() as client:
#         resp = await client.post(f"{EXPLAIN_URL}/explain", json=data)
#     return resp.json()
# # api/gateway_service/main.py
# from contextlib import asynccontextmanager
# from typing import Optional

# import httpx
# from fastapi import FastAPI, Request, HTTPException
# from fastapi.middleware.cors import CORSMiddleware

# PREDICT_URL = "http://localhost:8001"
# EXPLAIN_URL = "http://localhost:8002"

# TIMEOUT = httpx.Timeout(10.0, connect=5.0)
# RETRIES = 2  # simple manual retries

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Single shared client for connection reuse
#     app.state.client = httpx.AsyncClient(timeout=TIMEOUT)
#     yield
#     await app.state.client.aclose()

# app = FastAPI(
#     title="RetentionPulse Gateway",
#     description="Routes to prediction and explain microservices",
#     version="1.0.1",
#     lifespan=lifespan,
# )

# # CORS for local dev (add your prod origin here later)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# async def root():
#     return {"status": "ok", "services": {"predict": f"{PREDICT_URL}/predict",
#                                          "explain": f"{EXPLAIN_URL}/explain"}}

# async def _forward_json(method: str, url: str, payload: dict) -> dict:
#     last_exc: Optional[Exception] = None
#     for _ in range(RETRIES + 1):
#         try:
#             r = await app.state.client.request(method, url, json=payload)
#             if r.status_code >= 400:
#                 raise HTTPException(status_code=r.status_code, detail=r.text)
#             return r.json()
#         except Exception as e:
#             last_exc = e
#     # Surface a consistent 502 if upstream keeps failing
#     raise HTTPException(status_code=502, detail=f"Upstream error: {last_exc}")

# @app.post("/predict")
# async def proxy_predict(request: Request):
#     data = await request.json()
#     return await _forward_json("POST", f"{PREDICT_URL}/predict", data)

# @app.post("/explain")
# async def proxy_explain(request: Request):
#     data = await request.json()
#     return await _forward_json("POST", f"{EXPLAIN_URL}/explain", data)
# api/gateway_service/main.py
from contextlib import asynccontextmanager
from typing import Optional
import os

import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# --- Config (env overrides are great for Docker/Render) ---
PREDICT_URL = os.getenv("PREDICT_URL", "http://localhost:8001")
EXPLAIN_URL = os.getenv("EXPLAIN_URL", "http://localhost:8002")
# RETRIES = int(os.getenv("GATEWAY_RETRIES", "1"))

# TIMEOUT = httpx.Timeout(10.0, connect=5.0)
TIMEOUT = httpx.Timeout(connect=10.0, read=30.0, write=30.0, pool=5.0)
RETRIES = int(os.getenv("GATEWAY_RETRIES", "2"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # one shared HTTP client for connection reuse
    app.state.client = httpx.AsyncClient(timeout=TIMEOUT)
    try:
        yield
    finally:
        await app.state.client.aclose()

app = FastAPI(
    title="RetentionPulse Gateway",
    description="Routes to prediction and explain microservices",
    version="1.0.2",
    lifespan=lifespan,
)

# CORS for local dev; tighten in prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "status": "ok",
        "services": {
            "predict": f"{PREDICT_URL}/predict",
            "explain": f"{EXPLAIN_URL}/explain",
        },
    }

async def _forward(method: str, base_url: str, endpoint: str, request: Request) -> dict:
    """Forward JSON body + query params to an upstream service with basic retries."""
    params = dict(request.query_params)  # forwards e.g., top_k=6
    try:
        payload = await request.json()
    except Exception:
        payload = None

    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    last_exc: Optional[Exception] = None
    for _ in range(RETRIES + 1):
        try:
            resp = await app.state.client.request(method, url, params=params, json=payload)
            if resp.status_code >= 400:
                raise HTTPException(status_code=resp.status_code, detail=resp.text)
            return resp.json()
        except Exception as e:
            last_exc = e

    raise HTTPException(status_code=502, detail=f"Upstream error contacting {url}: {last_exc}")

@app.post("/predict")
async def proxy_predict(request: Request):
    return await _forward("POST", PREDICT_URL, "/predict", request)

@app.post("/explain")
async def proxy_explain(request: Request):
    return await _forward("POST", EXPLAIN_URL, "/explain", request)
