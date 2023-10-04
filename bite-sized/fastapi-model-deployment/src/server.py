from fastapi import FastAPI
import joblib

from src.serving_utils import preprocess_car_request, CarData

MODEL_PATH = 'models/linear_regression_pipeline.pkl'

app = FastAPI()

model = joblib.load(MODEL_PATH)


@app.get('/')
async def root() -> dict:
    return {'message': 'Hello World'}


@app.post('/predict')
async def score(data: CarData) -> dict:
    """
    Main prediction endpoint.
    """

    preprocessed_data = preprocess_car_request(data)

    preds = model.predict(preprocessed_data)

    return {'predictions': str(preds[0])}
