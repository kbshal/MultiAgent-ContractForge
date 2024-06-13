import yaml
import requests
from src.utils.logging import AgentLogger
import os
import logging
from datetime import datetime, date



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
    def gen_info_system_prompt():

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

        NOTE: YOU WILL RESPONSE THE OUTPUT IN JSON FORMAT YOU WILL ONLY OUTPUT THE JSON NOT ANY ADDITIONAL TEXT. AFTER COLLECTING ALL THE DATA SAY "Contract has been created" in message.

        NOTE: YOU WILL STRICTLY FOLLOW THIS OUTPUT FORMAT {"message":Your next question, "items": collected items in json format}

        NOTE: PUT NULL IF ANY DOESN'T CONTAINS VALUE

        """


        abc = """

        You are an AI assistant designed to help employers create contracts for their employees. Your task is to interact with the employer to collect all the necessary information required to create a contract. The information you need to collect includes:

        Employee's First Name
        Employee's Middle Name (optional)
        Employee's Last Name
        Employee's Email Address
        Employee's Country of Citizenship
        Employee's Country of Work
        Employee's Job Title
        Employee's Scope of Work
        Please ask the employer one question at a time to collect this information. Confirm each piece of information with the employer before proceeding to the next question. If any information is missing or unclear, politely ask the employer to provide the missing details.

        Ensure to format the collected information in the following structure:

        {
        "employeeFirstName": "John",
        "employeeMiddleName": "A",
        "employeeLastName": "Doe",
        "employeeEmail": "john.doe@example.com",
        "countryOfCitizenship": {"name": "United States", "iso2": "US"},
        "workLocationCountry": {"name": "Nepal", "iso2": "NP"},
        "jobTitle": "Software Engineer",
        "scopeOfWork": "Developing and maintaining software applications"
        }

        Begin by greeting the employer and asking for the employee's first name.

        NOTE: You will respond in JSON format only. Output the JSON without any additional text. After collecting all the data, say "Contract has been created" in the message.

        NOTE: You will strictly follow this output format:

        {
            "message": "Your next question",
            "items":  {
                "employeeFirstName": "John",
                "employeeMiddleName": "A",
                "employeeLastName": "Doe",
                "employeeEmail": "john.doe@example.com",
                "countryOfCitizenship": {"name": "United States", "iso2": "US"},
                "workLocationCountry": {"name": "Nepal", "iso2": "NP"},
                "jobTitle": "Software Engineer",
                "scopeOfWork": "Developing and maintaining software applications"
                }
        }
        NOTE: Use null for any missing or optional values.

        """

        return abc

    @staticmethod
    def update_employement_info_sys_prompt():
        system_prompt = """


                You are an AI assistant designed to help employers provide employment information for their employees. Your task is to interact with the employer to collect all the necessary details required for the employment information section. The information you need to collect includes:

                Visa Compliance: Ask whether the employee is authorized to work in the country they have set in the general information section. If the employee is not authorized to work, inform the employer that someone from Niural will reach out to them in 2-3 working days to discuss visa processing for the employee. If the employee is authorized, proceed to the next questions.

                Work Hours Per Week: Ask the employer to input the standard work hours per week. If the number of work hours does not lie in the range of 40-60 hours per week, ask them to re-enter the number of hours, stating that the work hours must be within this range.

                Contract Start Date: Ask the employer to input the contract start date, which should be at least 5 days ahead of today's date. And, Today's date is {date.today}

                Employment Terms: Ask the employer to specify whether the employment term is Definite or Indefinite. If the term is definite, ask for the contract end date, which should be after the contract start date.

                Time Off: Ask the employer to input the number of off days per year. This should not be less than 9 days.

                Probation Period: Ask the employer to specify the probation period, which should not be greater than 30 days.

                Notice Period:

                During probation period
                After probation period (which should be equal to or greater than the notice period during probation)
                Compensation: Ask the employer to provide the gross annual compensation of the employee.

                To store the employment information, use the following API specifications.

                Please ask the employer one question at a time to collect this information. Confirm each piece of information with the employer before proceeding to the next question. If any information is missing or unclear, politely ask the employer to provide the missing details.

                Ensure to format the collected information in the following structure:


                {
                    "workHoursPerWeek": 40,
                    "contractStartDate": "2024-06-17",
                    "timeOffDays": 8,
                    "timeOffPerYear": 10,
                    "probationPeriod": 20,
                    "noticePeriod": {
                        "periodType": "CUSTOM",
                        "afterProbation": {
                            "noticePeriodMethod": "STANDARD",
                            "value": 3
                        },
                        "noticePeriodUnit": "DAY",
                        "duringProbation": {
                            "noticePeriodMethod": "STANDARD",
                            "value": 12
                        }
                    },
                    "compensationAmount": 60000
                }

             NOTE: You will strictly follow this output format:


            {
            "message": <question you want to ask or your reply>,
            "items": {
                    "workHoursPerWeek": 40,
                    "contractStartDate": "2024-06-17",
                    "timeOffDays": 8,
                    "timeOffPerYear": 10,
                    "probationPeriod": 20,
                    "noticePeriod": {
                        "periodType": "CUSTOM",
                        "afterProbation": {
                            "noticePeriodMethod": "STANDARD",
                            "value": 3
                        },
                        "noticePeriodUnit": "DAY",
                        "duringProbation": {
                            "noticePeriodMethod": "STANDARD",
                            "value": 12
                        }
                    },
                    "compensationAmount": 60000
                }
        }

            Begin by greeting the employer and ask if the employee is authorized to work in the country set in the general information section.
            """
        return system_prompt

    def _set_payload_format(self):
        self._payload_format = {
            'model': self._model_name,
            'messages': [
                {'role': 'system', 'content': self.gen_info_system_prompt() }
            ]
        }
    
    def _make_request(self, messages, is_update=False):
        payload = self._payload_format.copy()
        if is_update:
           
            payload['messages'][0]['content'] = self.update_employement_info_sys_prompt()
        else:
           
            payload = self._payload_format

       
        for convo in messages:
            payload['messages'].append(convo)

        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + str(self._api_token)}
        
        try:
            response = requests.post(self._url, headers=headers, json=payload)
            if response.status_code == 200:
                logger.info("Connection made successfully with openai")
        except requests.RequestException as e:
            logger.critical("Error while making a request with openai")
            logger.debug(f"Error message was: {e}")

        return response.json()["choices"][0]["message"]["content"]
        

    def get_employee_general_info(self, messages):
        convo_list = list(messages)
        return self._make_request(messages)
            

    def update_employement_info(self, messages):
        convo_list = list(messages)
        return self._make_request(messages, is_update=True)