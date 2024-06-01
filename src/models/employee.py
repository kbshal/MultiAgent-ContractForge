from pydantic import  constr, BaseModel, Field, EmailStr, conint, condate, validator


class EmployeeGeneralInfo(BaseModel):
    EmployeeFirstName: constr(min_length=1)
    EmployeeMiddleName: str = None
    EmployeeLastName: constr(min_length=1)
    EmployeeEmail: EmailStr
    EmployeecountryOfCitizenship: dict
    EmployeecountryOfWork: str
    EmployeejobTitle: constr(min_length=1)
    EmployeescopeOfWork: str

class Country(BaseModel):
    name: str
    iso2: str

class EmploymentInformation(BaseModel):
    visa_compliance: bool
    work_hours_per_week: conint(ge=40, le=60) = Field(..., description="Number of work hours per week must be between 40 and 60.")
    contract_start_date: condate()
    employment_terms: str = Field(..., description="Employment terms can be either Definite or Indefinite.")
    contract_end_date: Optional[condate()] = None
    time_off: conint(ge=9) = Field(..., description="Number of off days per year, should not be less than 9.")
    probation_period: conint(le=30) = Field(..., description="Probation period should not be greater than 30 days.")
    notice_period_during_probation: int
    notice_period_after_probation: int
    compensation: float

    @validator('contract_start_date')
    def validate_contract_start_date(cls, v):
        if v < date.today() + timedelta(days=5):
            raise ValueError('Contract start date should be at least 5 days ahead from today’s date.')
        return v

    @validator('employment_terms')
    def validate_employment_terms(cls, v, values):
        if v not in ["Definite", "Indefinite"]:
            raise ValueError("Employment terms can be either Definite or Indefinite.")
        if v == "Definite" and not values.get('contract_end_date'):
            raise ValueError("For definite employment terms, contract end date must be provided.")
        if values.get('contract_end_date') and values.get('contract_start_date') and values['contract_end_date'] <= values['contract_start_date']:
            raise ValueError("Contract end date should be after contract start date.")
        return v

    @validator('notice_period_after_probation')
    def validate_notice_period(cls, v, values):
        if 'notice_period_during_probation' in values and v < values['notice_period_during_probation']:
            raise ValueError('Notice period after probation should be equal to or greater than during probation.')
        return v