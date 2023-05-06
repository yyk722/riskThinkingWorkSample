from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 6),
    'retries': 0
}

dag = DAG(
    'workSample_bash',
    default_args=default_args,
    description='A simple DAG to run 3 Python scripts in sequence',
    schedule_interval="0 * * * *",
)

t1 = BashOperator(
    task_id='raw_data_process',
    bash_command='python app/raw_data_process.py',
    dag=dag,
)

t2 = BashOperator(
    task_id='feature_engineer',
    bash_command='python app/feature_engineer.py',
    dag=dag,
)

t3 = BashOperator(
    task_id='model_training',
    bash_command='python app/model_training.py',
    dag=dag,
)

t1 >> t2 >> t3
