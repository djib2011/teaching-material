import pytest
import pandas as pd

from main import train, predict


class ModelMock:

    def __init__(self):
        self._trained = False

    def fit(self, data):
        self._trained = True
        return self

    def predict(self, data):
        return [0] * len(data)


@pytest.fixture(scope='module')
def model():
    return ModelMock()


@pytest.fixture(scope='module')
def data():
    return pd.DataFrame({'col1': [1, 2, 3], 'col2': [1, 2, 3], 'col3': [1, 2, 3]}) 


def test_train(data, model):

    model._trained = False  # make sure model is untrained
    train(data, model)

    assert model._trained  # check if model.fit is called 


def test_predct(data, model):

    preds = predict(data, model)
    assert len(preds) == len(data)  # check if model.predict is called

