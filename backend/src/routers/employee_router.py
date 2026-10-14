from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.services.employee_service import (create_employee as create_employee_service,
                                           update_employee as update_employee_service,
                                           delete_employee as delete_employee_service,
                                           get_employee_by_id as get_employee_by_id_service,
                                           get_employee_by_email as get_employee_by_email_service,
                                           get_all_employees as get_all_employees_service)

from src.schema.employee import (EmployeeResponse,
                                 EmployeeCreate, 
                                 EmployeeUpdate)

from src.lib.database import get_db

router = APIRouter()

#Cria o funcionário
@router.post("/employee/", response_model=EmployeeResponse)
def create_employee():

#Busca o funcionário pelo ID
@router.get("/employee/{employee_id}", response_model=EmployeeResponse)
def get_employee_by_id():

#Busca o funcionário pelo email
@router.get("/employee/{email}", response_model=EmployeeResponse)
def get_employee_by_email():

#Busca todos os funcionários
@router.get("/employee/", response_model=List[EmployeeResponse])
def get_all_employees():

#Atualiza um funcionário específico
@router.put("/employee/{employee_id}", response_model=EmployeeResponse)
def update_employee():

#Deleta um funcionário específico
@router.delete("/employee/{employee_id}", response_model=EmployeeResponse)
def delete_employee():