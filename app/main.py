from fastapi import FastAPI

from app.core.config import settings
from app.db.database import engine
from app.db.base import Base
from app.models.employee import Employee
from app.api.routes.employee import router as employee_router

app = FastAPI(title=settings.APP_NAME)

# Development only: create tables automatically
Base.metadata.create_all(bind=engine)

app.include_router(employee_router)


@app.get("/")
def home():

    return {
        "message": "Employee Management API is running"
    }