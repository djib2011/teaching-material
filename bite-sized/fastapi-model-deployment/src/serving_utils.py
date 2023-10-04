import pandas as pd
from pydantic import BaseModel
from typing import List


class CarData(BaseModel):
    Location: str
    Year: int
    Kilometers_Driven: int
    Fuel_Type: str
    Transmission: str
    Owner_Type: str


def preprocess_car_request(data: CarData):
    """
    Preprocess the car request data before making predictions.
    """

    fields = [
        data.Location,
        data.Year,
        data.Kilometers_Driven,
        data.Fuel_Type,
        data.Transmission,
        data.Owner_Type,
    ]

    feature_names = ['Location', 'Year', 'Kilometers_Driven', 'Fuel_Type', 'Transmission', 'Owner_Type']

    return pd.DataFrame([fields], columns=feature_names).fillna(0)
