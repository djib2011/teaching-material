from datetime import datetime
import pandas as pd
import argparse
import os

from utils import LOGGER


def download_data(date: str = None, num_days: int = 1, long: float = 23.798, lat: float = 38.021) -> pd.DataFrame:
    """
    Function to download hourly temperatures for a given place and time range

    :param date: reference date, i.e. last date of the time period for which we will get the data
    :param num_days: number of days back to retrieve the data
                     (e.g. if num_days=3, we will get data for 3 days before the reference data)
    :param long: longitude of the position we want to get the temperatures
    :param lat: latitude of the position we want to get the temperatures
    """

    end_date = date or str(datetime.today().date())
    start_date = str((pd.Timestamp(end_date) - pd.Timedelta(days=num_days)).date())

    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current=temperature_2m&hourly=temperature_2m&timezone=Europe%2FMoscow&start_date={start_date}&end_date={end_date}&format=csv'

    return pd.read_csv(url, skiprows=6)


def convert_to_series(data: pd.DataFrame) -> pd.Series:
    """
    Convert the dataframe in to a series, indexed by the time
    """

    return data.set_index(pd.to_datetime(data['time']))['temperature_2m (°C)']


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


def get_last_timesteps(timeseries: pd.Series, lookback: int = 24) -> pd.Series:
    """
    Get the last lookback timesteps, so that the model can perform inference on them later on
    """

    return timeseries.sort_index().tail(lookback)


def save_outputs(X: pd.DataFrame, y: pd.DataFrame, last_X: pd.DataFrame):
    """
    Save the training dataframes
    """

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_outputs')

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    X.to_csv(os.path.join(output_dir, 'X.csv'))
    y.to_csv(os.path.join(output_dir, 'y.csv'))
    last_X.to_csv(os.path.join(output_dir, 'last_X.csv'))


def run_download_and_preprocess(date: str = None, num_days: int = 1, lookback: int = 24, horizon: int = 6):
    """
    Main entrypoint function for downloading and preprocessing weather data
    """

    LOGGER.info('Downloading data from weather API...')
    data = download_data(date=date, num_days=num_days)  # download data
    LOGGER.debug(f'{len(data) = }')

    LOGGER.info('Converting data to series...')
    series = convert_to_series(data)  # convert to timeseries
    LOGGER.debug(f'{series.shape = }')

    LOGGER.info(f'Extracting the last {lookback} hours from the series for inference...')
    last_X = get_last_timesteps(series, lookback=lookback)
    LOGGER.debug(f'{last_X.shape = }')

    LOGGER.info('Building the training dataset...')
    X, y = build_dataset(series, lookback=lookback, horizon=horizon)  # build training dataset
    LOGGER.debug(f'{X.shape = }')
    LOGGER.debug(f'{y.shape = }')

    LOGGER.info('Saving outputs to ./temp_outputs')
    save_outputs(X, y, last_X)  # save tables


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--date', type=str, required=False, default=None,
                        help='Reference date. I.e. last day of the timeseries')
    parser.add_argument('--num-days', type=int, required=False, default=1,
                        help='Number of days to include in the dataset')
    parser.add_argument('--lookback', type=int, required=False, default=24,
                        help='How many hours in the past should the model consider when making its forecast')
    parser.add_argument('--horizon', type=int, required=False, default=6,
                        help='How many hours into the future should the model predict')

    args = parser.parse_args()

    LOGGER.info('Running download and preprocessing')
    LOGGER.info(f'Command line arguments: {args}')

    run_download_and_preprocess(date=args.date, num_days=args.num_days, lookback=args.lookback, horizon=args.horizon)
