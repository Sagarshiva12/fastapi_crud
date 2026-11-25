from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.employee import Employee


def create_employee(db: Session, employee_data: dict):

    employee = Employee(**employee_data)

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


def get_all_employees(db: Session):

    query = select(Employee)

    return db.scalars(query).all()


def get_employee_by_id(db: Session, employee_id: int):

    query = select(Employee).where(Employee.id == employee_id)

    return db.scalar(query)


def get_employee_by_email(db: Session, email: str):

    query = select(Employee).where(Employee.email == email)

    return db.scalar(query)


def update_employee(db: Session, employee: Employee, update_data: dict):

    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee


def delete_employee(db: Session, employee: Employee):

    db.delete(employee)
    db.commit()

    return True