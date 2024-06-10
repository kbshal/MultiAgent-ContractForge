from fastapi import APIRouter
import json
from src.llm.contract_agent import ContractAgent
from src.utils.validations import verify_dictionary
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
    to_be_verified = json.loads(response)['items']
    verify_dict = verify_dictionary(dict(to_be_verified))
    if verify_dict['action']:
        print("Okay verified!")
        # now call the api to call the general info 
   
    return output
