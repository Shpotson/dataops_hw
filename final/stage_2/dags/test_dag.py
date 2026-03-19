from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def hello_world():
    print("Hello Airflow!")

dag = DAG(
    'my_test_dag',
    start_date=datetime(2026, 3, 19),
    schedule_interval='* * * * *',
    catchup=False
)

task = PythonOperator(
    task_id='hello_task',
    python_callable=hello_world,
    dag=dag
)