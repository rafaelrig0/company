from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.schema.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate, PhoneCreate, PhoneResponse, PhoneUpdate
from src.models.employee import Employee, Phones, Role
from pydantic import EmailStr

from src.lib.security import hash_password

from src.exceptions import NotFoundError, EmailAlreadyExistsError, PermissionDeniedError

ROLES_CHECK = {
    Role.DIRECTOR: {Role.DIRECTOR, Role.LEADER, Role.EMPLOYEE},
    Role.LEADER: {Role.LEADER, Role.EMPLOYEE},
    Role.EMPLOYEE: set(),
    }

def permission_check(current_user: Employee, role: Role) -> None:
    allowed = ROLES_CHECK.get(current_user.role, set())
    
    if role not in allowed:
        raise PermissionDeniedError

def create_check(current_user: Employee, new_employee: EmployeeCreate) -> None:
    permission_check(current_user, new_employee.role)

def delete_check(current_user: Employee, target: Employee) -> None:
    if current_user.role != Role.DIRECTOR:
        raise PermissionDeniedError
    if current_user.employee_id == target.employee_id:
        raise PermissionDeniedError

def update_check(current_user: Employee, target: Employee, changes: dict) -> None:
    if current_user.role == Role.EMPLOYEE:
        raise PermissionDeniedError
    permission_check(current_user, target.role)

    updated_role = changes.get("role")
    if updated_role is not None:
        permission_check(current_user, updated_role)

def create_employee(db: Session, current_user: Employee, new_employee: EmployeeCreate) -> Employee:
    create_check(current_user, new_employee)
    if db.query(Employee).filter(Employee.email == new_employee.email).first():
        raise EmailAlreadyExistsError
    
    db_employee = Employee(fullname=new_employee.fullname,
                           email=new_employee.email,
                           phones=[Phones(phone_number=p.phone_number) for p in new_employee.phones],
                           role=new_employee.role,
                           password=hash_password(new_employee.password),
                           salary=new_employee.salary,
                           department=new_employee.department,
                           )
    
    db.add(db_employee)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise EmailAlreadyExistsError
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, current_user: Employee, employee_id: int, updated_employee: EmployeeUpdate) -> Employee:
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not db_employee:
        raise NotFoundError

    changes = updated_employee.model_dump(exclude_unset=True, exclude_none=True)
    update_check(current_user, db_employee, changes)

    email = changes.get("email", None)
    if email and email != db_employee.email:
        if db.query(Employee).filter(Employee.email == email).first():
            raise EmailAlreadyExistsError

    password = changes.pop("password", None)
    if password:
        db_employee.password = hash_password(password)

    phones = changes.pop("phones", None)
    if phones is not None: 
        db_employee.phones = [Phones(phone_number=p["phone_number"]) for p in phones]

    for field, value in changes.items():
        setattr(db_employee, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise EmailAlreadyExistsError
    db.refresh(db_employee)
    return db_employee
    
def delete_employee(db: Session, current_user: Employee, employee_id: int):
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not db_employee:
        raise NotFoundError
    delete_check(current_user, db_employee)
    db.delete(db_employee)
    db.commit()
    return db_employee

def get_employee_by_id(db: Session, employee_id: int):
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not db_employee:
        raise NotFoundError
    return db_employee

def get_employee_by_email(db: Session, employee_email: EmailStr):
    db_employee = db.query(Employee).filter(Employee.email == employee_email).first()
    if not db_employee:
        raise NotFoundError
    return db_employee

def get_all_employees(db: Session, skip: int = 0, limit: int = 100):
    db_all_employees = db.query(Employee).offset(skip).limit(limit).all()
    return db_all_employees