from fastapi.testclient import TestClient
from titanic_api import app
import pytest

client = TestClient(app)


@pytest.fixture
def valid_passenger_data():
    return {'pclass': 3,
            'name': 'Braund, Mr. Owen Harris',
            'sex': 'male',
            'age': 22.0,
            'sibsp': 1,
            'parch': 0,
            'ticket': 'A/5 21171',
            'fare': 7.25,
            'cabin': 'C148',
            'embarked': 'S'}


def test_root_endpoint():
    """
    Test that a root endpoint is properly set up
    """
    response = client.get('/')
    assert response.status_code == 200


def test_predict_endpoint(valid_passenger_data):
    """
    Test that the predict endpoint works with valid data
    """
    response = client.post('/predict', json=valid_passenger_data)
    assert response.status_code == 200
    assert isinstance(response.json()['survived'], bool)  # ensure correct prediction output format


#
def test_predict_missing_fields(valid_passenger_data):
    """
    Test with missing fields in the request data
    """
    incomplete_data = valid_passenger_data.copy()
    del incomplete_data['age']  # delete the age field from the data

    response = client.post('/predict', json=incomplete_data)
    assert response.status_code == 422


def test_predict_invalid_data_types(valid_passenger_data):
    """
    Test with invalid data types
    """
    invalid_data = valid_passenger_data.copy()
    invalid_data['age'] = 'twenty nine'  # change age to an invalid data type

    response = client.post('/predict', json=invalid_data)
    assert response.status_code == 422


def test_predict_out_of_range_data(valid_passenger_data):
    """
    Test out-of-range data
    """
    invalid_data = valid_passenger_data.copy()
    invalid_data['fare'] = -10  # set fare to a negative number to simulate out-of-range data

    response = client.post('/predict', json=invalid_data)
    assert response.status_code == 400
