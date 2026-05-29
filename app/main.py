'''
this is the main entry point of the application.
It initializes the FastAPI app, sets up the database tables, and defines a root endpoint to check if the API is running.
to run the application, use the command: 
    uv run uvicorn app.main:app --reload
'''
from fastapi import FastAPI

#importing the database base and engine to create tables
from app.database.base import Base
from app.database.connection import engine

# Import models so SQLAlchemy registers them
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.discharged_patient import DischargedPatient
from app.models.idle_queue import IdleQueue

# Importing the doctor routes to include them in the application
from app.routes.doctor_routes import router as doctor_router

# Importing the patient routes to include them in the application
from app.routes.patient_routes import router as patient_router

app = FastAPI(
    #minor customization of the auto-generated API docs in the swagger UI
    #things can still run without any of these parameters but it just looks good to have all this info in the docs
    title="Dispatch",
    description="Priority-Aware Doctor Allocation System",
    version="1.0.0"
)


# Create database tables
Base.metadata.create_all(bind=engine)
'''
when you run the above line

SQLAlchemy:
   1 scans registered models,
   2 collects table definitions,
   3 generates SQL,
   4 creates actual SQLite tables.
'''

# Root endpoint to check if the API is running
@app.get("/")
def root():
    return {
        "message": "Dispatch API is running"
    }

# Include the doctor routes in the main application
app.include_router(doctor_router)

# Include the patient routes in the main application
app.include_router(patient_router)