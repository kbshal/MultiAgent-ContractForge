import yaml
import requests
from src.utils.logging import AgentLogger


logger = AgentLogger()

def load_config():
    with open(os.path.join.dirname(__file__), '../../config.yaml', 'r') as f:
        return yaml.safe_load(f)

def load_secrets():
    with open(os.path.join.dirname(__file__), '../../secrets.yaml', 'r') as f:
        return yaml.safe_load(f)



secrets = load_secrets()
config  = load_config()


class AIException(Exception):
    def __init__(self):
        super().__init__("Some error accoured while making connection with openai")

class ContractAgent(object):

    def __init__(self):
        self._url = config['opsenai_url']
        self._api_token = secrets['openai_api_token']
        self._set_payload_format()

    @staticmethod
    def system_prompt():
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
            "countryOfWork": "United States",
            "jobTitle": "Software Engineer",
            "scopeOfWork": "Developing and maintaining software applications"
        }

        Begin by greeting the employer and ask for the employee's first name.

        You will return like this {"message":"You will leave here the new question or initial question", "items": collected information in json format like above}

        """

        return system_prompt

    def _set_payload_format(self):
        self._payload_format = {
            'model': self._model_name,
            'messages': [
                {'role': 'system', 'content': self.system_prompt() }
            ]
        }
    
    def _make_request(self, convo_list):
        payload = self._payload_format
        for convo in convo_list:
            payload['messages'].append(convo)

        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + str(self._api_token)}
        
        try:
            response = requests.post(self._url, headers=headers, json=payload)
            
        except Exception as err:
            logger.critical(f"Error occured while requesting the API  Error message:{err}")
        try:
            response.raise_for_status()
            if response.status_code == 200:
                logger.success("Request was successfully with openai")
            response_data = response.json()
            return response_data["choices"][0]["message"]["content"]

        except requests.RequestException as e:
            logger.critical("Error while making an response with openai")
            logger.debug(f"Error message was:{e}")

    def get_employee_general_info(self, convo_list):
        convo_list = list(convo_list)
        return self._make_request(convo_list)
            