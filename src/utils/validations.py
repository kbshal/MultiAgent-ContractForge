from pydantic import ValidationError
from src.models.employee import EmployeeGeneralInfo
from src.models.employee import EmploymentInformation


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



general_info = {
    "contractType": "EOR",
    "contractTitle": "<Full name> - <Job title>", 
    "entityName": "Niural Inc",
    "countryOfCitizenship": {
        "name": "<name of the country of citizenship>", 
        "iso2": "<iso2-alpha-code-of the country of citizenship>"
    },
    "employeeEmail": "<email address of the employee>",
    "employeeFirstName": "<first name of the employee>",
    "employeeLastName": "<last name of the employee>", 
    "employeeMiddleName": "<middle name of the employee>", 
    "entityIncorporationLocation": {
        "addressLine1": "865 Market Street San Francisco Centre",
        "city": "San Francisco",
        "country": {
            "name": "United States", 
            "iso2": "US"
        },
        "state": {
            "name": "California", 
            "iso2": "CA", 
            "label": "California"
        },
        "zipcode": "94103"
    },
    "entityName": "Niural Inc",
    "entityRepresentativeEmail": "suraj@niural.com",
    "entityRepresentativeName": "Zeppy Test",
    "entityType": "Limited liability company (LLC)",
    "jobTitle": "<job title of the employee>",
    "niuralEntityToUse": "NIURAL_INC",
    "scopeOfWork": "<scope of work>",
    "workLocationCountry": {
        "name": "<name of the work country>", 
        "iso2": "<iso2-alpha-code of the work country>"
    }
}

info = {"employeeFirstName":"Bishal","employeeMiddleName":"Kharal","employeeLastName":"Kharal","employeeEmail":"flkajfdl@gmail.com","countryOfCitizenship":{"name":"United States","iso2":"US"},"workLocationCountry":{"name":"Nepal","iso2":"NP"},"jobTitle":"Engineer","scopeOfWork":"Software Engineering"}

def update_general_info(general_info, info):
    for key, value in info.items():
        if key in general_info:
            if isinstance(general_info[key], dict):
        
                update_general_info(general_info[key], value)
            elif isinstance(general_info[key], str):
              
                for placeholder, actual_value in info.items():
                    placeholder = f"<{placeholder}>"
                    if placeholder in general_info[key]:
                        general_info[key] = general_info[key].replace(placeholder, str(actual_value))
            else:
               
                general_info[key] = value
        else:
            general_info[key] = value

   
    for key, value in general_info.items():
        if isinstance(value, dict):
            update_general_info(value, info)


def update_general_info(general_info, info):
    # Special handling for composite placeholders like "<Full name> - <Job title>"
    full_name = f"{info.get('employeeFirstName', '')} {info.get('employeeMiddleName', '')} {info.get('employeeLastName', '')}".strip()
    job_title = info.get('jobTitle', '')
    if full_name and job_title:
        general_info['contractTitle'] = f"{full_name} - {job_title}"

    # Update general_info with values from info
    for key, value in info.items():
        if isinstance(value, dict):
            # Update nested dictionaries directly if they exist in general_info
            if key in general_info and isinstance(general_info[key], dict):
                general_info[key].update(value)
        else:
            # Replace placeholders in string values or update top-level keys
            for g_key, g_value in general_info.items():
                if isinstance(g_value, str) and f"<{key}>" in g_value:
                    general_info[g_key] = g_value.replace(f"<{key}>", str(value))
                elif key == g_key:
                    general_info[g_key] = value

# Assuming general_info and info are defined as shown
update_general_info(general_info, info)

# Print the updated general_info to verify the changes
print(general_info)




