#routes for patient related operations

#importing necessary modules and functions
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

#importing the get_db function from the database connection module to manage database sessions.
from app.database.connection import get_db
#importing models to interact with db
from app.models.patient import Patient
from app.services.intake_service import intake_patient
from app.schemas.patient_schema import (
    GPAssessment,
    PatientCreate,
    PatientResponse
)
#importing discharge service function to handle patient discharge after treatment is completed.
from app.services.discharge_service import (
    discharge_patient
)

#importing the DischargedPatientResponse schema to structure the response for discharged patient data.
from app.schemas.discharged_patient_schema import (
    DischargedPatientResponse
)

#importing the assess_patient function from the assessment service to handle patient assessment and potential referral to specialists.
from app.services.assessment_service import (
    assess_patient
)

#APIRouter is a class from FastAPI that allows you to create modular route handlers.
router = APIRouter(
    prefix="/patient",
    tags=["Patients"]
)

'''========================================================================================================================'''
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

'''========================================================================================================================'''
# this endpoint handles the assessment of patients by a GP, including updating the patient's diagnosis notes,
# department needs, triage level, and reassigning them to a specialist doctor if necessary
@router.put(
    "/assess/{patient_id}",
    response_model=DischargedPatientResponse

)
def gp_assessment(
    patient_id: int,
    assessment: GPAssessment,
    db: Session = Depends(get_db)
):

    return assess_patient(
        db=db,
        patient_id=patient_id,
        diagnosis_notes=assessment.diagnosis_notes,
        requires_specialist=assessment.requires_specialist,
        department_needed=assessment.department_needed,
        triage_level=assessment.triage_level
    )

'''========================================================================================================================'''
# this endpoint handles the discharge of patients after treatment is completed
@router.put(
    "/discharge/{patient_id}", #the patient_id is passed as a path parameter to identify which patient is being discharged
    response_model=DischargedPatientResponse
)
def discharge_patient_route(
    patient_id: int, #the id of the patient being discharged, extracted from the path parameter
    db: Session = Depends(get_db)# creates a database session using the get_db function and injects the dependency
):
    # the discharge_patient function is called to handle the business logic of patient discharge
    discharged_patient = discharge_patient(
        db=db,
        patient_id=patient_id
    )
    return discharged_patient
