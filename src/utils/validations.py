from pydantic import ValidationError
from src.models.employee import EmployeeGeneralInfo
from src.models.employee import EmploymentInformation
from constants import ROOT_DIR
import os 
import json


class UpdateGeneralInfoException(Exception):
    def __init__(self):
        super().__init__("Something wrong occured while update the complete genral info")


class NiuralException(Exception):
    def __init__(self):
        self.__init__("Error while making request to Niural Server")

    
def employment_info_validator(data):
    try:
        employment = EmploymentInformation(**data)
        return employment.dict()
    except ValidationError as err:
        return str(err)


def verify_dictionary(input_dict) -> dict:
    
    expected_keys = [
        "employeeFirstName",
        "employeeMiddleName",
        "employeeLastName",
        "employeeEmail",
        "countryOfCitizenship",
        "workLocationCountry",
        "jobTitle",
        "scopeOfWork"
    ]
    
    error_occurred = False
    error_message = ""
    

    for key in expected_keys:
        if key not in input_dict:
            error_occurred = True
            error_message += f"Missing key: {key}\n"
    
    action_needed = not error_occurred

    response = {
        "message": error_message.strip(),
        "action": action_needed
    }

    return response
       

def update_general_info(general_info:dict) ->dict :
    try:
        general_info = dict(general_info)
        with open(os.path.join(ROOT_DIR, 'templates/employee_general_info.json')) as f:
            complete_general_info = json.loads(f.read())

        for key, value in general_info.items():
            complete_general_info[key] = general_info[key]
            if value is None:
                complete_general_info[key] = "null"
                continue
        complete_general_info['contractTitle'] = general_info['employeeFirstName'] + " " + general_info['employeeLastName'] + " - " + general_info['jobTitle']

        return complete_general_info
    except Exception as err:
        raise UpdateGeneralInfoException(err)
        


    

    





