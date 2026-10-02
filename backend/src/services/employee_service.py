from sqlalchemy.orm import Session

from src.schema.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate, PhoneCreate, PhoneResponse, PhoneUpdate
from src.models.employee import Employee, Phones, Role

from src.lib.security import hash_password, verify_password, need_rehash

from src.exceptions import NotFoundError, EmailAlreadyExistsError, PermissionDeniedError

def create_employee(db: Session, employee: EmployeeCreate, phones: PhoneCreate):
    existing_employee = db.query(Employee).filter(Employee.email == employee.email).first()
    if existing_employee:
        raise EmailAlreadyExistsError

    employee.password = 
    
    db_employee = Employee(fullname=employee.fullname,
                           email=employee.email,
                           phones=list[phones.phone_number],
                           role=employee.role,
                           password=employee.password_hash,
                           salary=employee.salary,
                           department=employee.department,
                           )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: int, id: int, employee: EmployeeUpdate, phones: PhoneUpdate):
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not db_employee:
        raise NotFoundError

    db_employee.fullname = employee.fullname
    db_employee.email = employee.email
    for phone in employee.phones:
        new_phone = Phones(phone_number = phone.phone_number,
                           employee_id = db_employee.employee_id
        )
        db.add(new_phone)
    db_employee.role = employee.role
    db_employee.password_hash = employee.password_hash
    db_employee.salary = employee.salary
    db_employee.department = employee.department

def delete_employee(db: Session):
def get_employee_by_id(db: Session):
def get_employee_by_email(db: Session):
def get_all_employees(db: Session):