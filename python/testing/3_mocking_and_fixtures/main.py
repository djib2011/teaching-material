import pandas as pd
import pickle


def load_data(data_path):
    return pd.read_csv(data_path)


def load_model(model_path):
   return pickle.load(open(model_path, 'rb')) 


def train(data, model):
    return model.fit(data)


def predict(data, model):
    return model.predict(data)

