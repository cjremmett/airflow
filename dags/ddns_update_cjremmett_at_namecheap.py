from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
import pendulum
from airflow.models import Variable
import re

def ddns_update_cjremmett_at_namecheap():
    namecheap_password = Variable.get("namecheap_password")
    domain_name = 'cjremmett.com'
    host = '@'
    ip_address = get_public_ip()
    if not is_valid_ipv4(ip_address):
        raise Exception(ip_address + ' was found to be an invalid IPv4 address. Did not update NameCheap DNS.')
    response = requests.get(f'https://dynamicdns.park-your-domain.com/update?host={host}&domain={domain_name}&password={namecheap_password}&ip={ip_address}')
    if response.status_code > 201:
        raise Exception('API call failed. Status code: ' + str(response.status_code))


def is_valid_ipv4(ip_string):
    """
    Checks if a string contains a valid IPv4 address using a regular expression.

    Args:
        ip_string: The string to check.

    Returns:
        True if the string contains a valid IPv4 address, False otherwise.
    """

    # Regex for IPv4 address
    ipv4_regex = r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"

    # Search for the pattern in the string
    match = re.search(ipv4_regex, ip_string)

    return bool(match)


def get_public_ip() -> str:
    response = requests.get('https://dynamicdns.park-your-domain.com/getip')
    return response.text
    

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