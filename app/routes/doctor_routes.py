'''this file defines the API routes related to doctor operations'''

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Importing the get_db function from the database connection module to manage database sessions.
from app.database.connection import get_db
from app.models.doctor import Doctor
from app.schemas.doctor_schema import (
    DoctorCreate,
    DoctorResponse
)

# APIRouter is a class from FastAPI that allows you to create modular route handlers.
# It helps in organizing the routes for different parts of the application using prefixes and tags.
router = APIRouter(
    prefix="/doctor",
    tags=["Doctors"]
)

# This route handler is responsible for adding a new doctor to the database.
@router.post(
    "/add",# The endpoint for adding a doctor is defined as "/add" under the "/doctor" prefix, resulting in "/doctor/add".   
    response_model=DoctorResponse  #response model
)
def add_doctor(
    doctor: DoctorCreate, # pydantic validation model for incoming request data
    db: Session = Depends(get_db) #FastAPI will automatically call the get_db function to provide a database session when this route is accessed.
    # Dependency injection is a design pattern that allows you to define dependencies for your functions or classes and have them automatically provided when needed.

):
    
    #new doctor instance made using pydantic validation model for doctor creation
    new_doctor = Doctor(
        doctor_name=doctor.doctor_name,
        department=doctor.department,
        max_patient_limit=doctor.max_patient_limit
    )

    # Add the new doctor to the database
    db.add(new_doctor)

    #commit the transaction to save the new doctor in the database.
    # Until this point, the new doctor is only staged in the session and not yet persisted in the database.
    db.commit()

    # Refresh the instance to get the updated data from the database,
    db.refresh(new_doctor)

    # Return the newly created doctor as a response, which will be serialized according to the DoctorResponse schema.
    return new_doctor