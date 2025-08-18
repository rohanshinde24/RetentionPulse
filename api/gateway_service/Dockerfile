FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PREDICT_URL=http://prediction:8001 \
    EXPLAIN_URL=http://explain:8002

WORKDIR /app

COPY api/requirements.txt api/requirements.txt
RUN pip install --no-cache-dir -r api/requirements.txt

COPY api /app/api

ENV PYTHONPATH=/app/api

EXPOSE 8000
CMD ["uvicorn", "gateway_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
