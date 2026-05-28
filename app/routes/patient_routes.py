#routes for patient related operations

#importing necessary modules and functions
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

#importing the get_db function from the database connection module to manage database sessions.
from app.database.connection import get_db
#importing models to interact with db
from app.models.patient import Patient
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

def add_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):

    new_patient = Patient(
        patient_name=patient.patient_name,
        issue=patient.issue
    )

    # After creating the new patient object, we add it to the database session, 
    db.add(new_patient)

    #commit the transaction to save it to the database, 
    db.commit()

    #refresh the instance to get any updated fields (like the auto-generated id).
    db.refresh(new_patient)

    #returing the newly created patient object
    return new_patient