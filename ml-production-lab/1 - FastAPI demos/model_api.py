from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import numpy as np
import pickle
import os

app = FastAPI()

# Load the pre-trained model
# Note: this object is actually a sklearn Pipeline; it contains all preprocessing steps as well as the model.
script_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(script_dir, 'resources/iris_model.pkl'), 'rb') as f:
    model = pickle.load(f)

# Names of the classes in the iris dataset
iris_target_names = ['setosa', 'versicolor', 'virginica']


# Define a data model for input validation
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.get('/')
async def root():
    """
    Root endpoint
    """
    return {'message': 'Welcome to the iris prediction service!'}


@app.post('/predict')
async def predict(iris_input: IrisInput):
    """
    Main model inference endpoint
    """

    # Convert input data to the expected format for the model
    data = np.array([[
        iris_input.sepal_length,
        iris_input.sepal_width,
        iris_input.petal_length,
        iris_input.petal_width
    ]])

    # Perform inference
    prediction = model.predict(data)

    # Decode model prediction
    predicted_class = iris_target_names[prediction[0]]

    return {'predicted_class': predicted_class}


@app.get('/model-info')
async def model_info():
    """
    Endpoint providing info on the model and its hyperparameters
    """
    return {step.__class__.__name__: step.get_params() for name, step in model.steps}
