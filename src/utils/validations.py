from pydantic import ValidationError
from src.models.employee import EmployeeGeneralInfo


def employee_general_info_validator(data):
    try:
        employee = EmployeeGeneralInfo(**data)
        return employee.dict()
    except ValidationError as err:
        return str(err)