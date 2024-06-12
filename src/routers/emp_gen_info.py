from fastapi import APIRouter
import json
from src.llm.contract_agent import ContractAgent
from src.utils.validations import verify_dictionary, update_general_info, UpdateGeneralInfoException, NiuralException
from src.api.callapi import store_gen_info
from src.utils.logging import AgentLogger
from pydantic import BaseModel
from typing import List
import json



contract_agent = ContractAgent()
logger = AgentLogger()
router  = APIRouter()

class Messsage(BaseModel):
    role: str
    content: str

class MessagePayload(BaseModel):
    messages: list[Messsage]

@router.post("/gen_info/")
def general_info(messages: MessagePayload):
    messages = messages.dict()
    messages_only = messages["messages"]
    #print(messages)
    response = contract_agent.get_employee_general_info(messages=messages_only)
    
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

    try:
        if verify_dict['action']:
            try:
                complete_general_info = update_general_info(to_be_verified)
                logger.info("User submitted values validated!")
                #print(complete_general_info)
                try: 
                    response = store_gen_info(complete_general_info)
                    message.update({"server":response['message']}) # for patch request
                except NiuralException as nerr:
                    logger.critical(f"Error occured while making request to niural server {nerr}")
                    message = {"message":"Something wrong while making request to niural server"}
            except UpdateGeneralInfoException:
                message = {"message":"something went wrong while updating the general info. Please try again."}
    except Exception as err:
        print(f"{err} occured")
        pass

    return message



   
