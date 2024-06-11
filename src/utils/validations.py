from pydantic import ValidationError
from src.models.employee import EmployeeGeneralInfo
from src.models.employee import EmploymentInformation
from constants import ROOT_DIR


def employee_general_info_validator(data):
    try:
        employee = EmployeeGeneralInfo(**data)
        return employee.dict()
    except ValidationError as err:
        return str(err)

    
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
    with open(os.path.join(ROOT_DIR, 'templates/employee_general_info.json')) as f:
        complete_general_info = f.read()

    for key in general_info.keys():
        complete_general_info[key] = general_info[key]

    return complete_general_info


    

    





