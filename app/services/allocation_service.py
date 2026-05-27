# This module contains the core logic for allocating patients to doctors based on their department and current patient load.

#importing the Session class from SQLAlchemy to manage database sessions and transactions.
from sqlalchemy.orm import Session

#importing models to interact with db
from app.models.doctor import Doctor
from app.models.patient import Patient


#the function to allocate a patient to an available doctor based on the department needed and triage level.
def allocate_patient(
    db: Session,# database session passed as an argument to perform db operations
    patient_name: str,# name of the patient to be allocated
    department_needed: str,# department in which the patient needs to be treated, used to find doctors in the same department
    triage_level: int #severity of patient's condition. lower the number higher the urgency
):
    
    # Query the database to find doctors in the required department who have not yet reached their maximum patient limit.
    available_doctors = (
        db.query(Doctor)
        .filter(
            Doctor.department == department_needed,
            Doctor.active_patients < Doctor.max_patient_limit
        )
        .order_by(Doctor.active_patients.asc()) # prioritize doctors with fewer active patients
        .all()# Retrieve all matching doctors as a list. If no doctors are available, this will return an empty list.
    )

    assigned_doctor = None

    # Check if there are any available doctors in the required department.
    if available_doctors:
        assigned_doctor = available_doctors[0]# the first doctor in the sorted list (the one with the least active patients) is selected for allocation.

        assigned_doctor.active_patients += 1

        patient_status = "assigned"

    # If no doctors are available, the patient will be marked as waiting for a doctor.
    else:
        patient_status = "waiting_for_doctor"

    # Create a new patient record in the database with the assigned doctor (if any) and the appropriate status.
    new_patient = Patient(
        patient_name=patient_name,
        department_needed=department_needed,
        assigned_doctor_id=(
            assigned_doctor.id
            if assigned_doctor
            else None
        ),
        triage_level=triage_level,
        status=patient_status
    )

    # Add the new patient to the database
    db.add(new_patient)

    #commit the transaction to save the new patient in the database.
    db.commit()

    # Refresh the instance to get the updated data from the database,
    db.refresh(new_patient)

    # Return the newly created patient as a response, which will be serialized according to the PatientResponse schema.
    return new_patient
'''
Nice
'''