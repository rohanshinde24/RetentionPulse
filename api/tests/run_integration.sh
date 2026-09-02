#!/usr/bin/env bash
set -euo pipefail

compose() { docker compose "$@"; }
cleanup() { compose logs --no-color || true; compose down --volumes --remove-orphans; }
trap cleanup EXIT

wait_for() {
  local url="$1"
  local name="$2"
  for _ in $(seq 1 90); do
    if curl --fail --silent "$url" >/dev/null; then
      return 0
    fi
    sleep 2
  done
  echo "Timed out waiting for ${name}: ${url}" >&2
  return 1
}

compose up --build --detach prediction explain gateway
wait_for http://localhost:8001/ "prediction service"
wait_for http://localhost:8002/ "explanation service"
wait_for http://localhost:8000/health "gateway"

predict=$(curl --fail --silent --show-error --request POST http://localhost:8000/predict --header 'Content-Type: application/json' --data @api/tests/fixtures/customer.json)
[[ "$predict" == *'"churn_probability"'* ]]

explain=$(curl --fail --silent --show-error --request POST 'http://localhost:8000/explain?top_k=3' --header 'Content-Type: application/json' --data @api/tests/fixtures/customer.json)
[[ "$explain" == *'"top_features"'* ]]

customers=$(curl --fail --silent --show-error 'http://localhost:8000/customers?page_size=1')
[[ "$customers" == *'"customer_id"'* ]]

customer_explain=$(curl --fail --silent --show-error 'http://localhost:8000/customers/7590-VHVEG/explain?top_k=3')
[[ "$customer_explain" == *'"top_features"'* ]]

upload=$(curl --fail --silent --show-error --request POST http://localhost:8000/predict/upload --header 'Content-Type: text/csv' --data-binary @api/tests/fixtures/customers.csv)
[[ "$upload" == *'"successful_rows":1'* ]]

echo "Integration checks passed."
