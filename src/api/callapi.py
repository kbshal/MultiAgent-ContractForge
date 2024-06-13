import requests
import yaml
import os
from src.utils.validations import NiuralException
from src.utils.logging import AgentLogger


logger = AgentLogger()

def load_config():
   with open(os.path.join(os.path.dirname(__file__), '../../config/config.yaml'), 'r') as f:
        return yaml.safe_load(f)

def load_secrets():
   with open(os.path.join(os.path.dirname(__file__), '../../config/secrets.yaml'), 'r') as f:
        return yaml.safe_load(f)

config  = load_config()
secrets = load_secrets()

def store_gen_info(data):
    url = config['general_info_submit_url']
    auth_token = secrets['auth_token']
    headers = {

        "Accept": "application/json, text/plain, */*",
        "Authorization": f'{{"token":"{auth_token}"}}',
        "Content-Type": "application/json; charset=UTF-8",
        "Referer": "https://qa.niural.com/"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        logger.debug("error while creating contract ")
        return {"message":response.json(), "status_code":response.status_code}
    
    logger.info("A contract has been created successfully!")
    return {"message":response.json(), "status_code":response.status_code}




def update_employment_info(contract_id, data):
    url = config['url']+f'/{contract_id}'
    auth_token = secrets['auth_token']
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f'{{"token":"{auth_token}"}}',
        "Content-Type": "application/json; charset=UTF-8",
        "Referer": "https://qa.niural.com/"
    }
    response = requests.patch(url, headers=headers, json=data)
    return response.json()