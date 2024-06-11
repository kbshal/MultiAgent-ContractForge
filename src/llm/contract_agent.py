import yaml
import requests
from src.utils.logging import AgentLogger
import os
import logging



logger = AgentLogger(name='contract_agent', level=logging.DEBUG) #logfile='logs/contract_agent.logs'

def load_config():
    with open(os.path.join(os.path.dirname(__file__), '../../config/config.yaml'), 'r') as f:
        return yaml.safe_load(f)

def load_secrets():
   with open(os.path.join(os.path.dirname(__file__), '../../config/secrets.yaml'), 'r') as f:
        return yaml.safe_load(f)


secrets = load_secrets()
config  = load_config()


class AIException(Exception):
    def __init__(self):
        super().__init__("Some error accoured while making connection with openai")

class ContractAgent(object):

    def __init__(self):
        self._url = config['openai_url']
        self._api_token = secrets['openai_api_token']
        self._model_name = config['model_name']
        self._set_payload_format()

    @staticmethod
    def system_prompt():

        final_output = {
                "items":{
                            "employeeFirstName": "John",
                            "employeeMiddleName": "A",
                            "employeeLastName": "Doe",
                            "employeeEmail": "john.doe@example.com",
                            "countryOfCitizenship": {"name": "United States", "iso2": "US"},
                            "workLocationCountry": {"name":"Nepal", "iso2": "NP"},
                            "jobTitle": "Software Engineer",
                            "scopeOfWork": "Developing and maintaining software applications"
                        }
                        }

        system_prompt = """

       You are an AI assistant designed to help employers create contracts for their employees. Your task is to interact with the employer to collect all the necessary information required to create a contract. The information you need to collect includes:

        1. Employee's First Name
        2. Employee's Middle Name (optional)
        3. Employee's Last Name
        4. Employee's Email Address
        5. Employee's Country of Citizenship
        6. Employee's Country of Work
        7. Employee's Job Title
        8. Employee's Scope of Work

        Please ask the employer one question at a time to collect this information. Confirm each piece of information with the employer before proceeding to the next question. If any information is missing or unclear, politely ask the employer to provide the missing details. 

        Ensure to format the collected information in the following structure:

        {
            "employeeFirstName": "John",
            "employeeMiddleName": "A",
            "employeeLastName": "Doe",
            "employeeEmail": "john.doe@example.com",
            "countryOfCitizenship": {"name": "United States", "iso2": "US"},
            "workLocationCountry": {"name":”Nepal”, "iso2": "NP"} },
            "jobTitle": "Software Engineer",
            "scopeOfWork": "Developing and maintaining software applications"
        }

        Begin by greeting the employer and ask for the employee's first name. 
        
        NOTE: YOU WILL RESPONSE THE OUTPUT IN JSON FORMAT YOU WILL ONLY OUTPUT THE JSON NOT ANY ADDITIONAL TEXT.

        NOTE: YOU WILL STRICTLY FOLLOW THIS OUTPUT FORMAT {"message":Your next question, "items": collected items in json format}

        NOTE: IF DATA IS NULL THE SIMPLY PUT VALUE null in string like this "null"
        """

        return system_prompt

    def _set_payload_format(self):
        self._payload_format = {
            'model': self._model_name,
            'messages': [
                {'role': 'system', 'content': self.system_prompt() }
            ]
        }
    
    def _make_request(self, messages):
        payload = self._payload_format
        for convo in messages:
            payload['messages'].append(convo)

        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + str(self._api_token)}
        
        try:
            response = requests.post(self._url, headers=headers, json=payload)
            if response.status_code == 200:
                logger.info("Connection made successfully with openai")
            response = response.json()

        except requests.RequestException as e:
            logger.critical("Error while making an response with openai")
            logger.debug(f"Error message was:{e}")

        return response["choices"][0]["message"]["content"]
        

    def get_employee_general_info(self, messages):
        convo_list = list(messages)
        return self._make_request(messages)
            