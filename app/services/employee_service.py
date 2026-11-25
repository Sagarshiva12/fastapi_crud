from sqlalchemy.orm import Session

from app.repositories import employee_repository as repository


def create_employee(db: Session, employee_data):

    existing = repository.get_employee_by_email(
        db, employee_data.email
    )

    if existing:
        raise ValueError("Employee email already exists")

    return repository.create_employee(
        db, employee_data.model_dump()
    )


def get_all_employees(db: Session):

    return repository.get_all_employees(db)


def get_employee(db: Session, employee_id: int):

    return repository.get_employee_by_id(db, employee_id)


def update_employee(db: Session, employee_id: int, employee_data):

    employee = repository.get_employee_by_id(db, employee_id)

    if not employee:
        return None

    update_data = employee_data.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing = repository.get_employee_by_email(
            db, update_data["email"]
        )

        if existing and existing.id != employee_id:
            raise ValueError("Email already belongs to another employee")

    return repository.update_employee(db, employee, update_data)


def delete_employee(db: Session, employee_id: int):

    employee = repository.get_employee_by_id(db, employee_id)

    if not employee:
        return False

    return repository.delete_employee(db, employee)