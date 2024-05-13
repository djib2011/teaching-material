import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from main import train, predict, get_data_from_api


class ModelMock:
    """
    Sample class we could create ourselves if we wanted to mock the model's behavior
    """
    
    def __init__(self):
        self._trained = False

    def fit(self, data):
        self._trained = True
        return self

    def predict(self, data):
        return [0] * len(data)


@pytest.fixture(scope='module')
def model():
    return MagicMock()


@pytest.fixture(scope='module')
def data():
    return pd.DataFrame({'col1': [1, 2, 3], 'col2': [1, 2, 3], 'col3': [1, 2, 3]}) 


def test_train(data, model):

    train(data, model)

    model.fit.assert_called_once()  # check if model.fit is called 


def test_predct(data, model):

    preds = predict(data, model)
    model.predict.assert_called_once()  # check if model.predict is called

@patch('main.requests.get')
def test_get_data_from_api_success(mock_get):

    #with patch('main.requests.get') as mock_get:

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'data': 'example'}

    result = get_data_from_api('https://api.example.com/data')

    assert result == {'data': 'example'}
    mock_get.assert_called_once_with('https://api.example.com/data')

