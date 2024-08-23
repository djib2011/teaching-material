from datetime import datetime
import pandas as pd
import argparse
import logging
import os


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

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    X.to_csv(os.path.join(output_dir, 'X.csv'))
    y.to_csv(os.path.join(output_dir, 'y.csv'))
    last_X.to_csv(os.path.join(output_dir, 'last_X.csv'))


def _create_logger() -> logging.Logger:
    """
    Create a logger for more convenient logging
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


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

    logger = _create_logger()  # create logger

    logger.info('Running download and preprocessing')
    logger.info(f'Command line arguments: {args}')

    logger.info('Downloading data from weather API...')
    data = download_data(date=args.date, num_days=args.num_days)  # download data
    logger.debug(f'{len(data) = }')

    logger.info('Converting data to series...')
    series = convert_to_series(data)  # convert to timeseries
    logger.debug(f'{series.shape = }')

    logger.info(f'Extracting the last {args.lookback} hours from the series for inference...')
    last_X = get_last_timesteps(series, lookback=args.lookback)
    logger.debug(f'{last_X.shape = }')

    logger.info('Building the training dataset...')
    X, y = build_dataset(series, lookback=args.lookback, horizon=args.horizon)  # build training dataset
    logger.debug(f'{X.shape = }')
    logger.debug(f'{y.shape = }')

    logger.info('Saving outputs to ./resources')
    save_outputs(X, y, last_X)  # save tables
