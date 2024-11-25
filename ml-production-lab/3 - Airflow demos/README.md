# Airflow demo

This demo will show the basics of creating Airflow DAGs.

## Airflow installation

Instructions for installing airflow can be found [here](https://github.com/codehub-learn/development-environment-setup/blob/main/python-ml-production-lab.md).

We will assume you've followed the docker installation of airflow and that it's built in the `airflow-build` directory. If this is done properly it should have created 4 subdirectories: `config`, `dags`, `logs` and `plugins`. Out of these we will make extensive use of `dags`.

## Dummy DAG

To check if airflow works we have a dummy DAG. Simply copy the script for `dummy_dag.py` in the `dags` directory mentioned above. Then go to the UI and you should be able to see this DAG:

![](https://github.com/codehub-learn/development-environment-setup/blob/main/images/ml-production-lab/ml-production-lab/dummy-dag-2.png?raw=true)

To run this DAG, you'll need to trigger it **manually**.

## Weather Forecasting DAG

This demo simulates a full ML pipeline. Its purpose is to train a forecaster on weather data retrieved from an API:

```
curl https://api.open-meteo.com/v1/forecast?latitude=38.021&longitude=23.798&current=temperature_2m&hourly=temperature_2m&timezone=Europe%2FMoscow&start_date=2024-08-21&end_date=2024-08-22&format=csv
```

It consists of 3 parts:
    1. Download and preprocess the weather API data
    2. Train the forecaster
    3. Generate a plot to visualize its performance

To run, you'll need to copy all files associated with the demo (`download_and_preprocess.py`, `generate_plot.py`, `train_model.py`, `utils.py` and `weather_forecasting_dag.py`) in the `dags` directory.
