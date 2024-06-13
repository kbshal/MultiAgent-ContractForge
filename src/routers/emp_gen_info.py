from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import json
import logging
import csv

from src.llm.contract_agent import ContractAgent
from src.utils.validations import UpdateGeneralInfoException, NiuralException, DataStoreException, UpdatePatchEmployementInfoException
from src.utils.utils import update_general_info, data_flattner_store, verify_update_emp_dict, verify_dictionary, patch_update_employeement_complete
from src.api.callapi import store_gen_info, update_employment_info
from src.utils.logging import AgentLogger


contract_agent = ContractAgent()
logger = AgentLogger()
router  = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class MessagePayload(BaseModel):
    messages: list[Message]


class UpdateEmployment(BaseModel):
    contract_id:str
    messages: list[Message]
    

@router.post("/gen_info/")
def general_info(messages: MessagePayload):
    messages = messages.dict()
    messages_only = messages["messages"]
    response = contract_agent.get_employee_general_info(messages=messages_only)
    message = {"message":response}
   
    try:
        if '{' in response: # if llm already gives in json format why to add another message key that's whys
            message = json.loads(response)
        else:
            message = {"message":response} # if it only contains the question
    except Exception:
        pass

    try:
        to_be_verified = json.loads(response)['items'] # get the contract items
    except Exception:
        pass
   
    try:
        verify_dict = verify_dictionary(dict(to_be_verified))
    except Exception as err:
        logger.info("Either something wrong while parsing user submitted data or it's going on.")
    print(response)

    try:
        if verify_dict['action']:
            try:
                complete_general_info = update_general_info(to_be_verified)
                logger.info("User submitted values validated!")
                #print(complete_general_info)
                try: 
                    response = store_gen_info(complete_general_info) # catch the respone from niural server while storing the data
                    data_to_store = dict(response['message']['data'])
                    message.update({"contract_id":data_to_store['contract_id']})
                    print(type(data_to_store))
                    try:
                        data_flattner_store(data_to_store)
                        logger.info("Successfully stored user contract data.")
                    except Exception:
                        logger.error(f"Failed to store user contract data due to an error: {e}")
                        message = {"message":"Error while storing your data"}
                        raise DataStoreException
                except NiuralException as nerr:
                    logger.critical(f"Request to niural server failed with error: {nerr}")
                    message = {"message":"Something wrong while making request to niural server"}
            except UpdateGeneralInfoException:
                message = {"message":"something went wrong while updating the general info. Please try again."}
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        pass

    return message

@router.patch("/update_employement/")
def update_employment(items: UpdateEmployment):
    items = items.dict()
    contract_id = items['contract_id']
    messages = items['messages']
    response = contract_agent.update_employement_info(messages)
    {"message":response}

    try:
        if '{' in response: # if llm already gives in json format why to add another message key that's whys
            message = json.loads(response)
        else:
            message = {"message":response} # if it only contains the question
    except Exception:
        pass

    try:
        to_be_verified = json.loads(response)['items'] # get the contract items
    except Exception:
        pass
    try:
        verify_dict = verify_update_emp_dict(dict(to_be_verified))
    except Exception as err:
        logger.info("Either something wrong while parsing user's data or it's going on")

    try:
        if verify_dict:
            try:
                complete_employment_update = patch_update_employeement_complete(contract_id, to_be_verified)
                logger.info("Got complete update patch json and validated!")

                try:
                    res = update_employment(contract_id, complete_employement_info)
                except NiuralException:
                    logger.debug("Error while making request to niural server [patch]")

            except UpdatePatchEmployementInfoException:
                logger.debug("Couldnt get the complete patch body json.")
            
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
    
    return message




   
