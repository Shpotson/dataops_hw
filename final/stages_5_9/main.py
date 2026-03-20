import json
import time
import logging
import asyncpg
import numpy as np
from typing import List
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from contextlib import asynccontextmanager

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('app.log')]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="ML Prediction Service")

# Глобальная переменная модели
model = None


class DummyModel:
    """Простая picklable модель"""

    def predict(self, X):
        return np.array([100000.0 + np.sum(X, axis=1) * 1000])


class PredictionRequest(BaseModel):
    features: List[float]


class PredictionResponse(BaseModel):
    prediction: float
    model_version: str = "1.0.0"


DB_CONFIG = {
    "host": "postgres", "port": 5432, "user": "mluser",
    "password": "mlpass", "database": "mldb"
}


async def get_db_connection():
    return await asyncpg.connect(**DB_CONFIG)


@app.on_event("startup")
async def startup_event():
    global model
    try:
        model = joblib.load("model.joblib")
        logger.info("Loaded pickled model")
    except:
        logger.info("Creating dummy model...")
        model = DummyModel()
        joblib.dump(model, "model.joblib")
        logger.info("Dummy model created")

    # Тест БД
    try:
        conn = await get_db_connection()
        await conn.execute(
            "CREATE TABLE IF NOT EXISTS predictions (id SERIAL PRIMARY KEY, request_data JSONB, prediction FLOAT, inference_time FLOAT, model_version VARCHAR(50), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        await conn.close()
        logger.info("Database ready")
    except Exception as e:
        logger.error(f"DB error: {e}")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "ready"}


@app.post("/api/v1/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(500, "Model not initialized")

    start_time = time.time()
    logger.info(f"📥 Predict: {request.features}")

    try:
        features = np.array(request.features).reshape(1, -1)
        prediction = model.predict(features)[0]
        inference_time = time.time() - start_time

        # Сохраняем в БД
        conn = await get_db_connection()
        await conn.execute(
            "INSERT INTO predictions (request_data, prediction, inference_time, model_version, created_at) VALUES ($1, $2, $3, $4, $5)",
            json.dumps(request.dict()), prediction, inference_time, "1.0.0", datetime.utcnow()
        )
        await conn.close()

        logger.info(f"📤 Prediction: {prediction:.2f}, time: {inference_time:.4f}s")
        return PredictionResponse(prediction=float(prediction))

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(500, str(e))