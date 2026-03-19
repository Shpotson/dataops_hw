FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir mlflow psycopg2-binary

RUN mkdir -p /mlflow/artifacts

ENV MLFLOW_BACKEND_STORE_URI=""
ENV MLFLOW_ARTIFACT_ROOT="/mlflow/artifacts"

EXPOSE 5000

CMD mlflow server \
    --backend-store-uri ${MLFLOW_BACKEND_STORE_URI} \
    --default-artifact-root ${MLFLOW_ARTIFACT_ROOT} \
    --host 0.0.0.0 \
    --port 5000