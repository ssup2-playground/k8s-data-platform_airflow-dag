from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

## Set default args
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 1, 1),
    'retries': 10,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval': '@hourly',
}

## Init dag
dag = DAG(
    "weather-southkorea-ingestor-synoptic",
    default_args=default_args,
)

ingestor = KubernetesPodOperator(
    dag=dag,
    name="hello-dry-run",
    image="debian",
    cmds=["bash", "-cx"],
    arguments=["echo", "10"],
    labels={"foo": "bar"},
    task_id="dry_run_demo",
    do_xcom_push=True,
)

ingestor