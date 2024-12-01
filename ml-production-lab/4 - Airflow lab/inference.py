import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle
import sys
import os

from download_symbol import download_historical_data
from utils import LOGGER


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_outputs')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')


def load_model() -> RandomForestRegressor:
    """
    Load the trained model
    """

    with open(os.path.join(DATA_DIR, 'trained_model.pkl'), 'rb') as f:
        model = pickle.load(f)

    return model


def make_inference(model: RandomForestRegressor, lookback_x: pd.DataFrame) -> np.ndarray:
    """
    Ask the trained model to make an inference on a given timeseries
    """

    # Timeseries needs to be scaled the same way as was the training data
    scaler = MinMaxScaler()
    lookback_x = scaler.fit_transform(lookback_x).T

    preds = model.predict(lookback_x)

    return scaler.inverse_transform(preds).flatten()  # bring preds back to their original scale


def generate_plot(lookback_x: pd.Series, preds: pd.Series, symbol: str):
    """
    Generate a plot of the historical data and the forecasts for a given stock
    """

    # Draw the plot
    lookback_x.plot(label='actual')
    preds.plot(label='preds')

    # Rotate the xticklabels
    plt.xticks(rotation=45)

    # Add a legend and a title
    plt.legend()
    plt.title(f'Stock price forecast for symbol {symbol}')

    # Save it to the output directory
    if not os.path.isdir(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    filename = os.path.join(OUTPUT_DIR, f'{symbol} {str(lookback_x.index[-1].date())}.png')
    LOGGER.info(f'Saving plot as {filename}')

    plt.savefig(filename)


def run_inference(symbol: str, lookback: int = 60):
    """
    Main entrypoint for generating predictions and plotting them
    """

    LOGGER.info('Loading trained model.')
    model = load_model()

    LOGGER.info(f'Downloading historical data for symbol {symbol}')
    data, dates = download_historical_data(symbol)

    if len(data) < lookback:
        LOGGER.error(f'Historical data for symbol {symbol} is less than required for desired lookback: {len(data)} < {lookback}')
        sys.exit()

    data = pd.DataFrame(data[-lookback:])
    dates = dates[-lookback:]

    LOGGER.info('Generating predictions for given timeseries.')
    preds = make_inference(model, data)

    data_series = pd.Series(data.values.flatten(), index=pd.to_datetime(dates))
    preds_series = pd.Series(preds, index=pd.date_range(start=dates[-1], periods=len(preds), freq='B'))  # count only business days

    generate_plot(data_series, preds_series, symbol)


if __name__ == '__main__':
    run_inference('MSFT')
