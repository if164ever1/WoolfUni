FROM apache/airflow:2.10.5-python3.12

COPY requirements.txt /tmp/hw07-requirements.txt
RUN pip install --no-cache-dir -r /tmp/hw07-requirements.txt \
    --constraint 'https://raw.githubusercontent.com/apache/airflow/constraints-2.10.5/constraints-3.12.txt'
