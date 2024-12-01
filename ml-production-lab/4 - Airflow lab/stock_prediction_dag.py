from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonVirtualenvOperator

TRAINING_SYMBOLS = Variable.get('TRAINING_SYMBOLS', default_var=['AAPL', 'MSFT', 'GOOG'], deserialize_json=True)
INFERENCE_SYMBOLS = Variable.get('INFERENCE_SYMBOLS', default_var=['AAPL', 'MSFT'], deserialize_json=True)


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
    import sys
    sys.path.append('/opt/airflow/dags')
    from training import run_training
    run_training()


def inference_callable(symbol: str):
    """
    Wrapper for run_inference function. Meant to be used from the AF PythonVirtualenvOperator
    """
    import sys
    sys.path.append('/opt/airflow/dags')
    from inference import run_inference
    run_inference(symbol)


# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 12, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# Virtualenv requirements
REQUIREMENTS = ['pandas==2.2.2', 'scikit-learn==1.5.1', 'matplotlib==3.9.2', 'requests==2.32.3']
PYTHON_VERSION = '3.11'

# Define the DAG
dag = DAG(
    'stock-prediction-dag',
    default_args=default_args,
    description='A DAG for daily stock price prediction',
    schedule_interval=timedelta(days=1),
    catchup=False)


# Define tasks
download_tasks = [PythonVirtualenvOperator(
                    task_id=f'download_symbol_{symbol}',
                    python_callable=download_symbol_callable,
                    op_args=[symbol],  # callable arguments
                    python_version=PYTHON_VERSION,
                    requirements=REQUIREMENTS,
                    dag=dag)
                  for symbol in TRAINING_SYMBOLS]

training_task = PythonVirtualenvOperator(
                        task_id='training',
                        python_callable=training_callable,
                        python_version=PYTHON_VERSION,
                        requirements=REQUIREMENTS,
                        dag=dag)

inference_tasks = [PythonVirtualenvOperator(
                      task_id=f'inference_{symbol}',
                      python_callable=inference_callable,
                      op_args=[symbol],  # callable arguments
                      python_version=PYTHON_VERSION,
                      requirements=REQUIREMENTS,
                      dag=dag)
                   for symbol in INFERENCE_SYMBOLS]

# Set task dependencies
download_tasks >> training_task >> inference_tasks
