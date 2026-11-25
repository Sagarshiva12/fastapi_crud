from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)
from app.services import employee_service

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.post("/", response_model=EmployeeResponse,
             status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    try:
        return employee_service.create_employee(db, employee)
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.get("/", response_model=list[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db)):

    return employee_service.get_all_employees(db)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = employee_service.get_employee(db, employee_id)

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee


@router.patch("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    try:
        updated = employee_service.update_employee(
            db, employee_id, employee
        )

        if not updated:
            raise HTTPException(status_code=404, detail="Employee not found")

        return updated

    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    deleted = employee_service.delete_employee(db, employee_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {"message": "Employee deleted successfully"}