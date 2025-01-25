# Weather SouthKorea Airflow DAG

## Python venv setup

Instructions for setting up a Python virtual environment for local development.

```bash
# Create virtual environment
$ python3 -m venv venv

# Activate virtual environment
$ source venv/bin/activate

# Install required packages
$ pip3 install -r requirements.txt

# Deactivate virtual environment when done
$ deactivate
```

## Create k8s secrets

* Data key

```bash
$ kubectl -n airflow create secret generic data-secret --from-literal=DATA_KEY=[data key]
```
