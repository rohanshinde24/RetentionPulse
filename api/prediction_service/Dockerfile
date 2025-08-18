FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_PATH=/app/api/models/model.pkl

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libgomp1 && \
    rm -rf /var/lib/apt/lists/*

COPY api/requirements.txt api/requirements.txt
RUN pip install --no-cache-dir -r api/requirements.txt

COPY api /app/api

ENV PYTHONPATH=/app/api

EXPOSE 8001
CMD ["uvicorn", "prediction_service.main:app", "--host", "0.0.0.0", "--port", "8001"]
