from pydantic import BaseModel, EmailStr, constr


class Employee(BaseModel):
    FirstName: constr(min_length=1)
    MiddleName: str = None
    LastName: constr(min_length1=1)
    Email: EmailStr
    countryOfCitizenship: dict
    countryOfWork: str
    jobTitle: constr(min_length=1)
    scopeOfWork: str
