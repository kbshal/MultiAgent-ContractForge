import os
from constants import ROOT_DIR
import json
from src.utils.validations import UpdateGeneralInfoException, DataStoreException, UpdatePatchEmployementInfoException
import csv
import pandas as pd


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




# for patch tasks

def verify_update_emp_dict(input_dict) -> dict:
    
    expected_keys = [
        "workHoursPerWeek",
        "contractStartDate",
        "timeOffDays",
        "timeOffPerYear",
        "probationPeriod",
        "noticePeriod",
        "compensationAmount"
    ]

   
    error_occurred = False
    error_message = ""

    for key in expected_keys:
        if key not in input_dict:
            error_occurred = True
            error_message += f"Missing key: {key}\n"

   
    if "noticePeriod" in input_dict:
        required_notice_period_keys = ["periodType", "noticePeriodUnit"]
        if "afterProbation" in input_dict["noticePeriod"]:
            required_after_probation_keys = ["noticePeriodMethod", "value"]
            missing_after_probation_keys = [key for key in required_after_probation_keys if key not in input_dict["noticePeriod"]["afterProbation"]]
            if missing_after_probation_keys:
                error_occurred = True
                error_message += f"Missing keys in afterProbation: {' '.join(missing_after_probation_keys)}\n"
        if "duringProbation" in input_dict["noticePeriod"]:
            required_during_probation_keys = ["noticePeriodMethod", "value"]
            missing_during_probation_keys = [key for key in required_during_probation_keys if key not in input_dict["noticePeriod"]["duringProbation"]]
            if missing_during_probation_keys:
                error_occurred = True
                error_message += f"Missing keys in duringProbation: {' '.join(missing_during_probation_keys)}\n"

    action_needed = not error_occurred

    response = {
        "message": error_message.strip(),
        "action": action_needed
    }

    return response




    
def data_flattner_store(data: dict):
    flattened_data = {
        "employee_first_name": data["employee_first_name"],
        "employee_middle_name": data["employee_middle_name"],
        "employee_last_name": data["employee_last_name"],
        "employee_email": data["employee_email"],
        "country_of_citizenship_name": data["country_of_citizenship"]["name"],
        "country_of_citizenship_iso2": data["country_of_citizenship"]["iso2"],
        "work_location_country_name": data["work_location_country"]["name"],
        "work_location_country_iso2": data["work_location_country"]["iso2"],
        "job_title": data["job_title"],
        "scope_of_work": data["scope_of_work"],
        "niural_entity_to_use": data["niural_entity_to_use"],
        "entity_name": data["entity_name"],
        "entity_type": data["entity_type"],
        "entity_incorporation_country_name": data["entity_incorporation_location"]["country"]["name"],
        "entity_incorporation_country_iso2": data["entity_incorporation_location"]["country"]["iso2"],
        "entity_incorporation_state_name": data["entity_incorporation_location"]["state"]["name"],
        "entity_incorporation_state_iso2": data["entity_incorporation_location"]["state"]["iso2"],
        "entity_incorporation_address_line1": data["entity_incorporation_location"]["address_line1"],
        "entity_incorporation_city": data["entity_incorporation_location"]["city"],
        "entity_incorporation_zipcode": data["entity_incorporation_location"]["zipcode"],
        "entity_representative_name": data["entity_representative_name"],
        "entity_representative_email": data["entity_representative_email"],
        "contract_title": data["contract_title"],
        "contract_type": data["contract_type"],
        "local_currency": data["local_currency"],
        "PK": data["PK"],
        "SK": data["SK"],
        "employer_id": data["employer_id"],
        "contract_status": data["contract_status"],
        "eor_employee_id": data["eor_employee_id"],
        "contract_id": data["contract_id"],
        "is_generic_contract": data["is_generic_contract"],
        "niural_entity_id": data["niural_entity_id"],
        "created_date": data["created_date"],
        "updated_date": data["updated_date"]
    }

    csv_file = './db/data.csv'

    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=flattened_data.keys())
            writer.writeheader()

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=flattened_data.keys())
        writer.writerow(flattened_data)


def patch_update_employeement_complete(contract_id:str, to_add:dict):
    df = pd.read_csv("./db/data.csv")
    contract_id_to_find  = contract_id
    print("contract id is ", contract_id)
    filtered_df = df.query("contract_id == @contract_id_to_find")

    try:
        with open(os.path.join(ROOT_DIR, 'templates/employement_information.json')) as f:
            complete_employement_info = json.loads(f.read())

        for key, value in to_add.items():
            if key in complete_employement_info:
                if isinstance(value, dict):
                    complete_employement_info[key].update(value)  
                elif isinstance(value, list):
                    complete_employement_info[key].extend(value)
                else:
                    complete_employement_info[key] = value
            else:
                complete_employement_info[key] = value

        try:
           complete_employement_info['contractTitle'] = str(filtered_df['employee_first_name'].values[0]) + " "+  str(filtered_df['employee_middle_name'].values[0]) + " "+ str(filtered_df['employee_last_name'].values[0]) + " - " + str(filtered_df['job_title'].values[0])
           complete_employement_info['employeeFirstName'] = str(filtered_df['employee_first_name'].values[0])
           complete_employement_info['employeeLastName'] = str(filtered_df['employee_last_name'].values[0])
           complete_employement_info['employeeEmail'] = str(filtered_df['employee_email'].values[0])
           complete_employement_info['jobTitle'] = str(filtered_df['job_title'].values[0])
           complete_employement_info['scopeOfWork'] = str(filtered_df['scope_of_work'].values[0])
           complete_employement_info['workLocationCountry']['name'] = str(filtered_df['work_location_country_name'].values[0])
           complete_employement_info['workLocationCountry']["iso2"] = str(filtered_df['work_location_country_iso2'].values[0])
           complete_employement_info['countryOfCitizenship']['name'] = str(filtered_df['country_of_citizenship_name'].values[0])
           complete_employement_info['countryOfCitizenship']['iso2'] = str(filtered_df['country_of_citizenship_iso2'].values[0])
           complete_employement_info['employeeMiddleName'] = str(filtered_df['employee_middle_name'].values[0])
        except Exception as err:
            print(err)

        return complete_employement_info

    except Exception as err:
        print(err)
        raise UpdatePatchEmployementInfo()
        
        



