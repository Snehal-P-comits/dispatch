#routes for patient related operations

#importing necessary modules and functions
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

#importing the get_db function from the database connection module to manage database sessions.
from app.database.connection import get_db
#importing models to interact with db
from app.services.intake_service import intake_patient
from app.schemas.patient_schema import (
    PatientCreate,
    PatientResponse
)

#importing the allocation service function to allocate patients to doctors based on department and triage level.
from app.services.allocation_service import allocate_patient


#APIRouter is a class from FastAPI that allows you to create modular route handlers.
router = APIRouter(
    prefix="/patient",
    tags=["Patients"]
)

# this endpoint handles the intake of new patients
@router.post(
    "/add",
    response_model=PatientResponse
)

# the add_patient function is the route handler for the /add endpoint
def add_patient(
    patient: PatientCreate, #takes in patient details in the request body, validated against the PatientCreate schema
    db: Session = Depends(get_db) #creates a database session using the get_db function and injects the dependency
):
    
    #the intake_patient function is called to handle the business logic of patient intake
    return intake_patient(
        db=db,# database session to interact with the database
        patient_name=patient.patient_name,# name of the patient being intaken
        issue=patient.issue #the issue that the patient has
    )