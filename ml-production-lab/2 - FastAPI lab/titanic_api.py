import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
import pickle
import os

# Load the model
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'resources/titanic_model.pkl')
print(f'Loading trained model from {model_path}')

with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Create the FastAPI app
app = FastAPI()


# Define a request body model using Pydantic
class PassengerFeatures(BaseModel):
    pclass: int
    name: str
    sex: str
    age: Optional[float]
    sibsp: int
    parch: int
    ticket: str
    fare: float
    cabin: Optional[str]
    embarked: Optional[str]


def check_for_logical_consistency(data: pd.DataFrame) -> bool:
    """
    Check if data are consistent with a series of logical rules (e.g. age must be >=0) and rules based on what
    we've observed in the training distribution (e.g. largest observed number of siblings is 8, we'll make a rule
    that won't allow the number during inference to be > 20).

    Note: we can in theory have values out-of-distribution (e.g. outliers that we didn't observe during training),
          but having values too different from that is more likely an error than a genuine outlier, so we'll disallow it
    """

    return all([0 < data['age'] < 130,                 # 'age' is a reasonable number (training distribution: [0, 80])
                0 <= data['sibsp'] < 20,               # 'siblings/spouses' is a logical number (train: [0, 8])
                0 <= data['parch'] < 20,               # 'parents/children' is a logical number (train: [0, 6])
                0 <= data['fare'] < 6000,              # 'fare' is a logical number (train: [0, 512])
                data['sex'] in ('male', 'female'),     # 'sex' is one of the 2 values seen in the training set
                data['embarked'] in ('S', 'C', 'Q')])  # 'embarked' is one of the 2 values seen in the training set


@app.get('/')
async def root():
    """
    Root endpoint for welcoming the user to the service
    """
    return {'message': 'Welcome to the titanic survival prediction service!'}


@app.post('/predict')
async def predict(features: PassengerFeatures):
    """
    Main inference endpoint of the service

    This should:
        - accept a request containing the values of the features we want to feed to the model
        - transform the features according to what we did during preprocessing
        - pass the transformed features to the model
        - return the model's prediction to the user
    """

    # Convert input data to the appropriate format
    ## Convert the data to a dataframe. Note that we won't include the features we dropped during preprocessing
    input_data = pd.DataFrame(data=[[features.pclass, features.sex, features.age, features.sibsp,
                                     features.parch, features.fare, features.embarked]],
                              columns=['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked'])

    ## Check for logical consistency. If we have some logically inconsistent data (e.g. age < 0) return an error
    ## Note: A better way to handle this would be to use pydantic's validators, rather than writing our own function
    if not check_for_logical_consistency(input_data.iloc[0].to_dict()):
        raise HTTPException(status_code=400, detail='Invalid value in some field')

    ## Encode 'sex' column. This was manually endoded during preprocessing, so we need to handle it ourselves here
    input_data['sex'] = input_data['sex'].map({'male': 0, 'female': 1})

    # Make the prediction
    ## Note: the remaining preprocessing steps are now part of the sklearn pipeline,
    ##        so they should be handled automatically when making the prediction!
    prediction = model.predict(input_data)

    # Return the prediction
    return {'survived': bool(prediction[0])}


if __name__ == "__main__":
    uvicorn.run(app,)