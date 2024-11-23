from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import os

from utils import LOGGER


def load_data() -> (pd.DataFrame, pd.DataFrame, pd.Series):
    """
    Load the training and inference dataframes
    """

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_outputs')

    X = pd.read_csv(os.path.join(output_dir, 'X.csv'), index_col=0)
    y = pd.read_csv(os.path.join(output_dir, 'y.csv'), index_col=0)
    last_X = pd.read_csv(os.path.join(output_dir, 'last_X.csv'), index_col=0)

    return X, y, last_X


def preprocessing(X: pd.DataFrame, y: pd.DataFrame) -> (np.ndarray, np.ndarray):
    """
    Scale each series independently, so that points in each take values in [0, 1]
    """

    scaler = MinMaxScaler()

    X = scaler.fit_transform(X.T).T
    y = scaler.transform(y.T).T

    return X, y


def train_model(X: np.ndarray, y: np.ndarray, **hparams: dict) -> RandomForestRegressor:
    """
    Train the regressor on the training data
    """

    model = RandomForestRegressor(**hparams)

    model.fit(X, y)

    return model


def make_inference(model: RandomForestRegressor, last_X: pd.Series) -> pd.Series:
    """
    Ask the trained model to make an inference on a given timeseries
    """

    # Timeseries needs to be scaled the same way as was the training data
    scaler = MinMaxScaler()
    last_X = scaler.fit_transform(last_X).T

    preds = model.predict(last_X)

    return scaler.inverse_transform(preds)  # bring preds back to their original scale


def convert_preds_to_series(preds: np.ndarray, last_X: pd.Series) -> pd.Series:
    """
    Function to make preds a pd.Series with the proper time index
    """

    preds = preds.flatten()

    # Make a new time index for the preds, starting 1 hour after the last timestamp
    preds_time_index = pd.date_range(start=pd.to_datetime(last_X.index[-1]) + pd.Timedelta(hours=1),
                                     periods=len(preds), freq='h')

    preds_series = pd.Series(preds, index=preds_time_index)

    return preds_series


def save_preds(preds: pd.Series):
    """
    Save the preds
    """

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_outputs')

    preds.to_csv(os.path.join(output_dir, 'preds.csv'))


def run_training():
    """
    Main entrypoint function for training the weather forecasting model
    """

    LOGGER.info('Loading training and inference datasets...')
    X, y, last_X = load_data()
    LOGGER.debug(f'{X.shape = }')
    LOGGER.debug(f'{y.shape = }')
    LOGGER.debug(f'{last_X.shape = }')

    LOGGER.info('Run preprocessing on training data...')
    LOGGER.debug(f'Before: {X.max().max() = }  |  {X.min().min() = }')
    LOGGER.debug(f'Before: {y.max().max() = }  |  {y.min().min() = }')
    X, y = preprocessing(X, y)
    LOGGER.debug(f'After: {X.max().max() = }  |  {X.min().min() = }')
    LOGGER.debug(f'After: {y.max().max() = }  |  {y.min().min() = }')

    LOGGER.info('Training model...')
    model = train_model(X, y)

    LOGGER.info(f'Performing inference on last {len(last_X)} datapoints')
    preds = make_inference(model, last_X)
    LOGGER.debug(f'{preds.shape = }')

    LOGGER.info('Converting predictions to pandas series with proper time index...')
    preds = convert_preds_to_series(preds, last_X)

    LOGGER.info('Saving predictions to ./temp_outputs')
    save_preds(preds)


if __name__ == '__main__':

    run_training()
