from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import pickle
import os

from utils import LOGGER


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_outputs')


def load_data_symbol(symbol: str) -> (pd.DataFrame, pd.DataFrame):
    """
    Load the training dataframes for a given symbol
    """

    X = pd.read_csv(os.path.join(DATA_DIR, f'{symbol}_X.csv'), index_col=0)
    y = pd.read_csv(os.path.join(DATA_DIR, f'{symbol}_y.csv'), index_col=0)

    return X, y


def load_data_multiple() -> (pd.DataFrame, pd.DataFrame):
    """
    Search for all symbols under the DATA_DIR, load the individual datasets and merge them all together
    """

    symbols = set([f.split('_')[0] for f in os.listdir(DATA_DIR) if f.endswith('X.csv') and f.split('_')[0].isupper()])
    LOGGER.info(f'Symbols found: {symbols}')

    data, targets = [], []
    for symbol in symbols:
        x, y = load_data_symbol(symbol)
        data.append(x)
        targets.append(y)

    return pd.concat(data), pd.concat(targets)


def normalize_timeseries(x: pd.DataFrame, y: pd.DataFrame) -> (np.ndarray, np.ndarray):
    """
    Scale each series independently, so that points in each take values in [0, 1]
    """

    scaler = MinMaxScaler()

    x = scaler.fit_transform(x.T).T
    y = scaler.transform(y.T).T

    return x, y


def train_model(x: np.ndarray, y: np.ndarray, **hparams: dict) -> RandomForestRegressor:
    """
    Train the regressor on the training data
    """

    model = RandomForestRegressor(**hparams)

    model.fit(x, y)

    return model


def run_training(symbol: str = None):
    """
    Main entrypoint function for training the stock price forecaster
    """

    # Load data for a stock symbol
    # ...

    # Normalize this data
    # ...

    # Train the model
    # ...

    # Save the trained model
    LOGGER.info('Saving trained model to ./temp_outputs')
    with open(os.path.join(DATA_DIR, 'trained_model.pkl'), 'wb') as f:
        pickle.dump(model, f)


if __name__ == '__main__':
    run_training()
