''' this module contains the business logic for assessing a patient after the initial intake by a GP.
It handles the assignment of patients to specialist doctors based on their department needs and triage level,
as well as updating patient records accordingly. '''

#imprting the session class from SQLAlchemy to create a db session
from sqlalchemy.orm import Session

#importing the Doctor and Patient models to interact with the corresponding tables in the database
from app.models.doctor import Doctor
from app.models.patient import Patient

#importing the discharge_patient function from the discharge service to handle patient discharge if needed during the assessment process.
from app.services.discharge_service import (
    discharge_patient
)



# This function handles the assessment of a patient by a GP, including updating the patient's diagnosis notes,
# department needs, triage level, and reassigning them to a specialist doctor if necessary.
def assess_patient(
    db: Session,# database session to interact with the database
    patient_id: int,# the id of the patient being assessed
    diagnosis_notes: str,# the diagnosis notes from the GP's assessment
    requires_specialist: bool, # indicates whether the patient needs to be referred to a specialist based on the GP's assessment
    department_needed: str | None ,# the department that the patient needs to be referred to based on the GP's assessment
    triage_level: int | None #the triage level assigned to the patient based on the severity of their condition as determined by the GP's assessment
):
    
    #query to find the patient being assessed in the DB
    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    # If the patient is not found in the database,
    # we return None to indicate that the assessment cannot be completed.
    if not patient:
        return None
    
    #store the previous GP assignment before updating the patient record
    previous_gp_id = patient.assigned_doctor_id

    # GP finishes assessment and is ready to transfer patient to specialist if needed.
    if previous_gp_id:
        gp_doctor = (
            db.query(Doctor)
            .filter(Doctor.id == previous_gp_id)
            .first()
        )

        if gp_doctor and gp_doctor.active_patients > 0:
            gp_doctor.active_patients -= 1

    # query to find specialist doctor based on department needed and availability

    # GP resolved issue directly
    # 
    if not requires_specialist:
        patient.diagnosis_notes = diagnosis_notes
        db.commit()
        return discharge_patient(
            db=db,
            patient_id=patient.id
        )

    specialist = (
        db.query(Doctor)
        .filter(
            Doctor.department == department_needed,
            Doctor.active_patients < Doctor.max_patient_limit
        )
        .order_by(Doctor.active_patients.asc())
        .first()
    )

    # variables to hold the assigned specialist's doctor id and the patient's new status after assessment
    assigned_specialist_id = None
    patient_status = "waiting_for_doctor" # default status if no specialist is available

    # If a specialist doctor is available, we assign the patient to that specialist and increment the specialist's active patient count.
    if specialist:
        assigned_specialist_id = specialist.id
        specialist.active_patients += 1
        patient_status = "assigned"
#Nice
    # Update patient record with new details from the GP's assessment
    patient.diagnosis_notes = diagnosis_notes
    patient.department_needed = department_needed
    patient.triage_level = triage_level
    patient.assigned_doctor_id = assigned_specialist_id
    patient.status = patient_status

    # Save the updated patient record to the database
    db.commit()
    
    # Refresh the patient object to get the latest data from the database, including any changes made during the commit.
    db.refresh(patient)

    # Return the updated patient object after assessment and potential reassignment to a specialist doctor.
    return patient