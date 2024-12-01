from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator


STOCK_SYMBOL = ''  # select desired stock symbol


def download_symbol_callable(symbol: str):
    """
    Wrapper for run_download_symbol function. Meant to be used from the AF PythonVirtualenvOperator
    """
    import sys
    sys.path.append('/opt/airflow/dags')
    from download_symbol import run_download_symbol
    run_download_symbol(symbol)


def training_callable():
    """
    Wrapper for run_training function. Meant to be used from the AF PythonVirtualenvOperator
    """

    # Import and run training script's main function
    # ...



def inference_callable():
    """
    Wrapper for run_inference function. Meant to be used from the AF PythonVirtualenvOperator
    """

    # Import and run inference script's main function
    # ...


# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date':   # Add initial date
    'email_on_failure': False,
    'email_on_retry': False,
    'retries':  # Add number of retries
    'retry_delay': # Add retry delay
}

# Virtualenv requirements
REQUIREMENTS = ['pandas==2.2.2', 'scikit-learn==1.5.1', 'matplotlib==3.9.2', 'requests==2.32.3']
PYTHON_VERSION = '3.11'

# Define the DAG
dag = DAG(
    'stock-prediction-dag',
    default_args=default_args,
    description='A DAG for daily predicting the price of a stock',
    schedule_interval=  # Add the schedule interval for this DAG
    catchup=False)


# Define tasks
download_task = PythonVirtualenvOperator(
                    task_id=f'download_symbol_{STOCK_SYMBOL}',
                    python_callable=download_symbol_callable,
                    op_args=[STOCK_SYMBOL],  # callable arguments
                    python_version=PYTHON_VERSION,
                    requirements=REQUIREMENTS,
                    dag=dag)

training_task = PythonVirtualenvOperator(
                        task_id='training',
                        python_callable=training_callable,
                        python_version=PYTHON_VERSION,
                        requirements=REQUIREMENTS,
                        dag=dag)

inference_task = PythonVirtualenvOperator(
                      task_id=f'inference_{STOCK_SYMBOL}',
                      python_callable=inference_callable,
                      # do we need anything else here?
                      python_version=PYTHON_VERSION,
                      requirements=REQUIREMENTS,
                      dag=dag)

# Set task dependencies
download_task >> training_task >> inference_task
