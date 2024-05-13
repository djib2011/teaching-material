import pickle
import requests
import pandas as pd


def get_data_from_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def load_data(data_path):
    return pd.read_csv(data_path)


def load_model(model_path):
   return pickle.load(open(model_path, 'rb')) 


def train(data, model):
    return model.fit(data)


def predict(data, model):
    return model.predict(data)

