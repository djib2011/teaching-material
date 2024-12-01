from typing import List
import pandas as pd
import requests
import sys
import os

from utils import LOGGER


API_KEY = 'ASO2CTQZNW5VCSF2'


def download_historical_data(symbol: str) -> (List[float], List[str]):

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={API_KEY}'

    data = requests.get(url).json()

    dates = list(data['Time Series (Daily)'].keys())[::-1]

    LOGGER.info(f'Retrieved historical data for symbol {symbol} for dates from {dates[0]} to {dates[-1]} ({len(dates)} in total).')

    return [float(data['Time Series (Daily)'][date]['4. close']) for date in dates], dates


def build_dataset(timeseries: pd.Series, lookback: int = 24, horizon: int = 6) -> (pd.DataFrame, pd.DataFrame):
    """
    Build the dataset (i.e. X and y tables) according to a given lookback and forecasting horizon

    For a more in-depth look read this forecasting tutorial:
    https://github.com/djib2011/python_ml_tutorial/blob/master/notebooks/26_forecasting.ipynb
    """
    data = pd.concat([timeseries.shift(-i) for i in range(lookback+horizon)], axis=1).dropna()
    data.columns = range(-lookback, horizon)
    data.index = timeseries.index[-len(data):]
    return data.iloc[:, :lookback], data.iloc[:, lookback:]


def save_outputs(x: pd.DataFrame, y: pd.DataFrame, symbol: str):
    """
    Save the training dataframes
    """

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_outputs')

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    x.to_csv(os.path.join(output_dir, f'{symbol}_X.csv'))
    y.to_csv(os.path.join(output_dir, f'{symbol}_y.csv'))


def run_download_symbol(symbol, lookback: int = 60, horizon: int = 5):
    """
    Main entrypoint function for downloading and preprocessing stock data for a given symbol
    """

    LOGGER.info(f'Downloading data for symbol: {symbol}')
    data, _ = download_historical_data(symbol=symbol)  # download data (ignore dates)
    LOGGER.debug(f'{len(data) = }')

    LOGGER.info('Converting data to series...')
    series = pd.Series(data)  # convert to timeseries
    LOGGER.debug(f'{series.shape = }')

    if len(series) < lookback + horizon:
        LOGGER.error(f'Historical data for symbol {symbol} is less than required for desired lookback: {len(series)} < {lookback + horizon}')
        sys.exit()

    LOGGER.info('Building the training dataset...')
    X, y = build_dataset(series, lookback=lookback, horizon=horizon)  # build training dataset
    LOGGER.debug(f'{X.shape = }')
    LOGGER.debug(f'{y.shape = }')

    LOGGER.info('Saving outputs to ./temp_outputs')
    save_outputs(X, y, symbol)  # save tables


if __name__ == '__main__':
    run_download_symbol(symbol='AAPL')
    run_download_symbol(symbol='GOOG')
