from datetime import datetime, timedelta

from airflow import DAG
from airflow.kubernetes.secret import Secret
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

from kubernetes.client import models as k8s_models

## Set default args
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 10,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval': '@hourly',
}

## Init dag
dag = DAG(
    "weather-southkorea-ingestor-synoptic",
    default_args=default_args,
)

## Init operators
secret_aws_access_env = Secret(
    deploy_type="env",
    deploy_target="AWS_KEY_ACCESS",
    secret="aws-secret",
    key="AWS_KEY_ACCESS",
)

secret_aws_secret_env = Secret(
    deploy_type="env",
    deploy_target="AWS_KEY_SECRET",
    secret="aws-secret",
    key="AWS_KEY_SECRET",
)

secret_data_key_env = Secret(
    deploy_type="env",
    deploy_target="DATA_KEY",
    secret="data-secret",
    key="DATA_KEY",
)

synoptic_ingestor = KubernetesPodOperator(
    dag=dag,
    task_id="synoptic-ingestor",
    image="ghcr.io/ssup2-playground/weather-southkorea-injestor-synoptic:0.1",
    container_resources=k8s_models.V1ResourceRequirements(
        limits={"memory": "2Gi", "cpu": "500m"},
    ),
    env_vars={
        "AWS_REGION" : "ap-northeast-2",
        "AWS_S3_BUCKET" : "weather-southkorea-data",
        "AWS_S3_DIRECTORY" : "synoptic-houly",
        "REQUEST_DATE" : "{{ dag_run.logical_date.subtract(hours=1) | ds_nodash }}",
        "REQUEST_HOUR" : "{{ dag_run.logical_date.subtract(hours=1).hour }}",
    },
    secrets=[secret_aws_access_env, secret_aws_secret_env, secret_data_key_env],
)

## Run
synoptic_ingestor