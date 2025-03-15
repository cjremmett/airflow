from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
import pendulum
from airflow.models import Variable

def ddns_update_cjremmett_at_namecheap():
    namecheap_password = Variable.get("namecheap_password")
    domain_name = 'cjremmett.com'
    host = '@'
    ip_address = get_public_ip()
    response = requests.get(f'https://dynamicdns.park-your-domain.com/update?host={host}&domain={domain_name}&password={namecheap_password}&ip={ip_address}')
    if response.status_code > 201:
        raise Exception('API call failed. Status code: ' + str(response.status_code))


def get_public_ip() -> str:
    try:
        response = requests.get('https://dynamicdns.park-your-domain.com/getip')
        #return response.text
        return '1.1.1.1'
    except Exception as e:
        return None
    

dag = DAG(
    'ddns_update_cjremmett_at_namecheap',
    start_date=pendulum.datetime(2025, 3, 14, tz="America/New_York"),
    schedule='*/12 * * * *'
)


t1 = PythonOperator(
    task_id='ddns_update_cjremmett_at_namecheap',
    python_callable=ddns_update_cjremmett_at_namecheap,
    dag=dag
)

t1