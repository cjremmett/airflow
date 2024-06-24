from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
import pendulum
from airflow.models import Variable

def ioffice_manual_checkin_reminder():
    token = Variable.get("gafg_tools_token")
    response = requests.post('https://cjremmett.com/flask/gafg-tools/trigger-manual-checkin-reminder', headers={"token": token})
    if response.status_code > 201:
        raise Exception('API call failed. Status code: ' + str(response.status_code))


dag = DAG(
    'gafg_tools_checkin_reminder',
    start_date=pendulum.datetime(2024, 6, 20, tz="America/New_York"),
    schedule='0 8 * * *'
)


t1 = PythonOperator(
    task_id='ioffice_manual_checkin_reminder',
    python_callable=ioffice_manual_checkin_reminder,
    dag=dag
)

t1