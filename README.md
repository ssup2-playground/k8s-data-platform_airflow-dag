# Weather SouthKorea Airflow DAG

## Create k8s secrets

* AWS access key, AWS secret key

```bash
$ kubectl -n airflow create secret generic aws-secret --from-literal=AWS_KEY_ACCESS=[access key] --from-literal=AWS_KEY_SECRET=[secret key]
```

* Data key

```bash
$ kubectl -n airflow create secret generic data-secret --from-literal=DATA_KEY=[data key]
```