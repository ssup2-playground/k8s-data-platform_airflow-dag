from datetime import datetime, timedelta

from airflow import DAG
from airflow.kubernetes.secret import Secret
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

import pendulum
from kubernetes.client import models as k8s_models

## Init dag
dag = DAG(
    dag_id="southkorea-weather",
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "retries": 5,
        "retry_delay": timedelta(minutes=10),
    },
    start_date=datetime(2023, 1, 1, tzinfo=pendulum.timezone("Asia/Seoul")),
    schedule="@hourly",
    catchup=True,
    max_active_tasks=4,
)

## Init operators
secret_data_key_env = Secret(
    deploy_type="env",
    deploy_target="DATA_KEY",
    secret="data-secret",
    key="DATA_KEY",
)

ingestor = KubernetesPodOperator(
    dag=dag,
    task_id="ingestor",
    image="ghcr.io/ssup2-playground/southkorea-weather-data-ingestor:0.2.0",
    container_resources=k8s_models.V1ResourceRequirements(
        requests={"memory": "2Gi", "cpu": "500m"},
    ),
    env_vars={
        "MINIO_ENDPOINT" : "192.168.1.89:9000",
        "MINIO_ACCESS_KEY" : "root",
        "MINIO_SECRET_KEY" : "root123!",
        "MINIO_BUCKET" : "southkorea-weather",
        "MINIO_DIRECTORY" : "hourly-parquet",
        "REQUEST_DATE" : "{{ execution_date.subtract(hours=24) | ds_nodash }}",
        "REQUEST_HOUR" : "{{ execution_date.subtract(hours=24).hour }}",
    },
    secrets=[secret_data_key_env],
)

## Run
ingestor
