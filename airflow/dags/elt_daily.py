from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

REPO = "/opt/airflow/repo"
default_args = {"retries":1, "retry_delay": timedelta(minutes=3)}

with DAG(
    "elt_daily",
    start_date=datetime(2025,11,1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_snapshot_run_test",
        bash_command=f"cd {REPO}/dbt_project && dbt deps && dbt snapshot --profiles-dir . && dbt run --profiles-dir . && dbt test --profiles-dir ."
    )

    dbt_run
