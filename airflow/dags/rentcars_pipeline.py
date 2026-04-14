from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys

sys.path.append("/opt/airflow")

# CALLBACK
def failure_callback(context):
    print("Pipeline falhou")

# DEFAULT ARGS
default_args = {
    "owner": "hugo",
    "retries": 0, 
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": failure_callback,
}

with DAG(
    dag_id="rentcars_pipeline",
    default_args=default_args,
    description="Pipeline end-to-end Rentcars",
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["rentcars", "data-engineering"],
) as dag:

    run_pipeline = BashOperator(
        task_id="run_pipeline",
        bash_command="python /opt/airflow/pipeline/run_pipeline.py"
    )