from pydantic import ValidationError
from src.models.employee import EmployeeGeneralInfo
from src.models.employee import EmploymentInformation
from constants import ROOT_DIR
import os 
import json


class UpdateGeneralInfoException(Exception):
    def __init__(self):
        super().__init__("Something wrong occured while updating the complete general info")


class UpdatePatchEmployementInfoException(Exception):
    def __init(self):
        super().__init__("Something went wrong while updating the employment info")

class NiuralException(Exception):
    def __init__(self):
        super().__init__("Error while making request to Niural Server")


class DataStoreException(Exception):
    def __init__(self):
        super().__init__("Error while storing the data please try againa")



 
def employment_info_validator(data):
    try:
        employment = EmploymentInformation(**data)
        return employment.dict()
    except ValidationError as err:
        return str(err)



    

    





