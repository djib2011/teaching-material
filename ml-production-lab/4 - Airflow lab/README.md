# Airflow lab

In this lab we will try to solve the holy grail of forecasting: stock price prediction.

## Airflow installation

Instructions for installing airflow can be found [here](https://github.com/codehub-learn/development-environment-setup/blob/main/python-ml-production-lab.md).

We will assume you've followed the docker installation of airflow and that it's built in the `airflow-build` directory. If this is done properly it should have created 4 subdirectories: `config`, `dags`, `logs` and `plugins`. Out of these we will make extensive use of `dags`.

## Premise

We want to eventually build a pipeline that:

1. Downloads every day historical stock market data for multiple stocks.
2. Preprocesses them accordingly so that we have a training dataset for a ML model.
3. Trains a ML model on the historical stock market data.
4. Runs inference on a series of selected stocks
5. Generates plots for these inferences, so that we can easily see the model's forecast and decide whether to buy or sell ;)

## Tasks

### A. Create a DAG that runs the pipeline for a single stock

The DAG consists of 3 steps:

1. **download** (`download_symbol.py`): This script downloads and preprocesses the historical stock market data for a given stock symbol. This script is **complete**, so you **don't** need to make any modifications for this lab.
2. **training** (`training.py`): This script trains a model on historical stock market data. This script is **incomplete**. All helper functions are written, you just need to write `run_training`, which is the main entrypoint function for this script.
3. **inference** (`inference.py`): This script downloads and preprocesses the historical stock market data for given stock symbol and calls the previously trained model to generate predictions on this data.  This script is **complete**, so you **don't** need to make any modifications for this lab.

The DAG is defined in `stock_prediction_dag.py`. This script is **incomplete**. There are several parts of this script you'll need you modify for this to work.

### B. Modify the previous DAG to work for multiple stocks

For this task you'll need to modify the previous DAG so that it works for multiple stocks at the same time. Make all necessary modifications.

We want all download tasks to run in parallel, when finished run the training task and then run all inference tasks in parallel. The desired flow can be seen in the screenshot below.

![](https://github.com/djib2011/teaching-material/blob/master/ml-production-lab/4%20-%20Airflow%20lab/resources/stock-prediction-dag.png?raw=true)

### C. Modify the DAG so that it reads the stock symbols are configurable

The idea here is to be able to select the stocks used for training and inference without modifying the code.

One way to achieve this is through Airflow variables. The easiest way to set their values is through the UI: `Admin -> Variables`:

![](https://github.com/djib2011/teaching-material/blob/master/ml-production-lab/4%20-%20Airflow%20lab/resources/stock-symbol-variables.png?raw=true)

Add the values of these variables and make the necessary modifications to the code to read the variables and create the DAG dynamically.

## Running the DAG

If you've set up Airflow using docker compose, you'll need to copy all files associated with the demo (`download_symbol.py`, `inference.py`, `training.py`, `utils.py` and `stock_prediction_dag.py`) in the `dags` directory.
