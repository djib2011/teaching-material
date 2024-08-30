from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator


def download_and_preprocess_callable():
    """
    Wrapper for run_download_and_preprocess function. Meant to be used from the AF PythonVirtualenvOperator
    """
    from download_and_preprocess import run_download_and_preprocess
    run_download_and_preprocess()


def train_model_callable():
    """
    Wrapper for run_training function. Meant to be used from the AF PythonVirtualenvOperator
    """
    from train_model import run_training
    run_training()


def generate_plot_callable():
    """
    Wrapper for run_generate_plot function. Meant to be used from the AF PythonVirtualenvOperator
    """
    from generate_plot import run_generate_plot
    run_generate_plot()


# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Virtualenv requirements
REQUIREMENTS = ['pandas==2.2.2', 'scikit-learn==1.5.1', 'matplotlib==3.9.2']
PYTHON_VERSION = '3.11'

# Define the DAG
dag = DAG(
    'weather-forecasting-dag',
    default_args=default_args,
    description='A DAG for updating a weather forecaster daily',
    schedule_interval=timedelta(days=1),  # Schedule it to run once a day
    catchup=False,  # Skip backfill for all missed runs
)

# Define tasks
download_task = PythonVirtualenvOperator(
        task_id='download_and_preprocess',
        python_callable=download_and_preprocess_callable,
        python_version=PYTHON_VERSION,  # Set the Python version
        requirements=REQUIREMENTS,  # Specify any requirements needed
        dag=dag
    )

train_model_task = PythonVirtualenvOperator(
        task_id='train_model',
        python_callable=train_model_callable,
        python_version=PYTHON_VERSION,
        requirements=REQUIREMENTS,
        dag=dag
)

generate_plot_task = PythonVirtualenvOperator(
        task_id='generate_plot',
        python_callable=generate_plot_callable,
        python_version=PYTHON_VERSION,
        requirements=REQUIREMENTS,
        dag=dag
)

# Set task dependencies
download_task >> train_model_task >> generate_plot_task
