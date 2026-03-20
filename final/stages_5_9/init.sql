CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    request_data JSONB,
    prediction FLOAT,
    inference_time FLOAT,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);