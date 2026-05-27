#routes for patient related operations

#importing necessary modules and functions
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

#importing the get_db function from the database connection module to manage database sessions.
from app.database.connection import get_db
#importing models to interact with db
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


@router.post(
    "/add",# The endpoint for adding a patient is defined as "/add" under the "/patient" prefix, resulting in "/patient/add".
    response_model=PatientResponse
)

# This route handler is responsible for adding a new patient to the database and allocating them to an available doctor based on the department needed and triage level.
def add_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):
    
    # Call the allocation service to allocate the patient to an available doctor and create a new patient record in the database.
    return allocate_patient(
        db=db,
        patient_name=patient.patient_name,
        department_needed=patient.department_needed,
        triage_level=patient.triage_level
    )