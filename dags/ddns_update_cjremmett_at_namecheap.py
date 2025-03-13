from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
import pendulum
from airflow.models import Variable

def ddns_update_cjremmett_at_namecheap():
    token = Variable.get("ddns_token")
    domain_name = 'cjremmett.com'
    host = '@'
    # Need to use the internal IP of the server because if the public IP changed cjremmett.com will be unreachable
    internal_ip = '192.168.0.121'
    response = requests.put(f'http://{internal_ip}/flask/dynamic-dns/update-namecheap-dns-record?host={host}&domain_name={domain_name}', headers={"token": token})
    if response.status_code > 201:
        raise Exception('API call failed. Status code: ' + str(response.status_code))


dag = DAG(
    'ddns_update_cjremmett_at_namecheap',
    start_date=pendulum.datetime(2024, 6, 20, tz="America/New_York"),
    schedule='*/12 * * * *'
)


t1 = PythonOperator(
    task_id='ddns_update_cjremmett_at_namecheap',
    python_callable=ddns_update_cjremmett_at_namecheap,
    dag=dag
)

t1