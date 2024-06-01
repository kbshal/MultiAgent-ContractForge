from pydantic import ValidationError
from src.models.employee import Employee


def employee_data_validator(data):
    try:
        employee = Employee(**data)
        return employee.dict()
    except ValidationError as err:
        return str(err)