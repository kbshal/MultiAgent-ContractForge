from fastapi import APIRouter
import json
from src.llm.contract_agent import ContractAgent
from src.utils.validations import verify_dictionary, update_general_info
from pydantic import BaseModel
from typing import List
import json



contract_agent = ContractAgent()

router  = APIRouter()

class Messsage(BaseModel):
    role: str
    content: str

class MessagePayload(BaseModel):
    messages: list[Messsage]

@router.post("/gen_info/")
def general_info(messages: MessagePayload):
    messages = (messages.dict())["messages"]
    response = contract_agent.get_employee_general_info(messages=messages)
    output = json.loads(response)
    to_be_verified = json.loads(response)['items'] # get the contract items
    print(to_be_verified)
    verify_dict = verify_dictionary(dict(to_be_verified)) # it will return True if the agent generated dictionary is valid
    if verify_dict['action']:
        complete_general_info = update_general_info(to_be_verified)
       
   
    return output
