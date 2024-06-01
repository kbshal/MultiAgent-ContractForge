import requests
import yaml
import os


def load_config():
    with open(os.path.join.dirname(__file__), '../../config.yaml', 'r') as f:
        return yaml.safe_load(f)


config  = load_config()


def store_gen_info(data):
    url = config['api_url']
    auth_token = config['auth_token']
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f'{{"token":"{auth_token}"}}',
        "Content-Type": "application/json; charset=UTF-8",
        "Referer": "https://qa.niural.com/"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def update_employment_info(contract_id, data):
    url = config['url']+f'/{contract_id}'
    auth_token = config['auth_token']
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f'{{"token":"{auth_token}"}}',
        "Content-Type": "application/json; charset=UTF-8",
        "Referer": "https://qa.niural.com/"
    }
    response = requests.patch(url, headers=headers, json=data)
    return response.json()