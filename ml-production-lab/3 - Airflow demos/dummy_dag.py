from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'dummy_dag',
    default_args=default_args,
    description='A simple dummy DAG',
    schedule_interval=timedelta(days=1),  # Schedule it to run once a day
    catchup=False,  # Skip backfill for all missed runs
)

# Define tasks
start_task = DummyOperator(
    task_id='start',
    dag=dag,
)

task_1 = DummyOperator(
    task_id='task_1',
    dag=dag,
)

task_2 = DummyOperator(
    task_id='task_2',
    dag=dag,
)

end_task = DummyOperator(
    task_id='end',
    dag=dag,
)

# Set task dependencies
start_task >> task_1 >> task_2 >> end_task
