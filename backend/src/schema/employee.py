from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.models.employee import Role

class PhoneCreate(BaseModel):
    phone_number: str = Field(pattern=r"^\+[1-9]\d{1,14}$")

class PhoneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    phone_number: str

class PhoneUpdate(BaseModel):
    phone_number : str = Field(pattern=r"^\+[1-9]\d{1,14}$")

class EmployeeCreate(BaseModel):
    fullname: str = Field(min_length=3, max_length=120)
    email: EmailStr
    phones: list[PhoneCreate] = Field(default_factory=list)
    password_hash: str = Field(min_length=10, max_length=150)
    manager_id: int | None = None
    salary: Decimal = Field(ge=0, decimal_places=2, max_digits=10)
    department: str = Field(min_length=2, max_length=100)
    role: Role = Role.EMPLOYEE

class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    employee_id: int
    fullname: str 
    email: EmailStr
    phones: list[PhoneResponse]
    manager_id : int | None = None
    salary: Decimal
    department: str
    role: Role

class EmployeeUpdate(BaseModel):
    fullname: str | None = Field(min_length=3, max_length=120)
    email: EmailStr | None = None
    phones: list[PhoneCreate] | None = Field(default_factory=list)
    password_hash: str | None = Field(min_length=10, max_length=150)
    manager_id: int | None = None
    salary: Decimal | None = Field(ge=0, decimal_places=2, max_digits=10)
    department: str| None = Field(min_length=2, max_length=100)
    role: Role | None = None