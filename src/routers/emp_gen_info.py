from fastapi import APIRouter
from src.llm.contract_agent import ContractAgent


contract_agent = ContractAgent()

router  = APIRouter()


@router.post("/gen_info/")
def general_info(convo_list):
    response = contract_agent.get_employee_general_info(convo_list=convo_list)
    geninfo = response['items']
    print(geninfo)


