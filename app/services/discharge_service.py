''' this module contains the service function to discharge a patient after treatment is completed. '''

from sqlalchemy.orm import Session

#importing the Doctor and Patient models to interact with the corresponding tables in the database
from app.models import discharged_patient
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.discharged_patient import (
    DischargedPatient
)

# This function handles the discharge of a patient, updates the patient's status to "completed" and decrementing the active patient count for the assigned doctor if applicable.
def discharge_patient(
    db: Session, # database session to interact with the database
    patient_id: int # the id of the patient being discharged
):
    
    # query to find the patient being discharged in the DB
    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    # If the patient is not found in the database,
    # we raise a ValueError to indicate that the discharge cannot be completed.
    if not patient:
        raise ValueError("Patient not found")

    # Storing the assigned doctor's ID if patient was assigned to a doctor
    assigned_doctor_id = patient.assigned_doctor_id

    #remove patient from assigned doctor's active patient count if they were assigned to a doctor
    if assigned_doctor_id:

        doctor = (
            db.query(Doctor)
            .filter(Doctor.id == assigned_doctor_id)
            .first()
        )

        if doctor and doctor.active_patients > 0:
            doctor.active_patients -= 1

    # Archiving patient data
    discharged_patient = DischargedPatient(
        patient_name=patient.patient_name,
        issue=patient.issue,
        diagnosis_notes=patient.diagnosis_notes,
        department_needed=patient.department_needed,
        assigned_doctor_id=patient.assigned_doctor_id,
        triage_level=patient.triage_level
    )

    #add the discharged patient record
    db.add(discharged_patient)
    #flush to get the discharged patient id before deleting the original patient record
    db.flush()
    # refresh to get any updated fields (like the auto-generated id) for the discharged patient record
    db.refresh(discharged_patient)
    # delete the original patient record from the patients table
    db.delete(patient)
    # commit the transaction to save changes to the database
    db.commit()
    # return the discharged patient record to confirm successful discharge and provide details of the discharged patient.
    return discharged_patient