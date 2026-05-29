'''this module contains the logic for triaging patients and allocating specialists based on their needs and the current load on doctors.'''

#importing session from sqlalchemy to interact with the database and perform queries and updates on the Doctor and Patient models.
from sqlalchemy.orm import Session

#importing models to perform queries and updates on the Doctor and Patient tables in the database.
from app.models.doctor import Doctor
from app.models.patient import Patient

#this function takes in the database session, the department needed by the patient, and the triage level of the patient. It first tries to find an available specialist in the required department with the least number of active patients. If a specialist is found, it assigns the patient to that specialist and updates the patient's status to "assigned". If no specialist is available, it looks for a lower priority patient who is currently assigned to a doctor in the same department and has a higher triage level than the incoming patient. If such a patient is found, it pauses that patient's treatment, unassigns them from their doctor, and assigns the incoming patient to that doctor instead. The function returns the ID of the assigned specialist (if any) and the status of the patient (either "assigned" or "waiting_for_doctor").
def allocate_specialist(
    db: Session,
    department_needed: str,
    triage_level: int
):
    #query to find an available specialist in the required department with the least number of active patients
    specialist = (
        db.query(Doctor)
        .filter(
            Doctor.department == department_needed,
            Doctor.active_patients < Doctor.max_patient_limit
        )
        .order_by(Doctor.active_patients.asc())
        .first()
    )
    
    #variables to store the ID of the assigned specialist (if any) and the status of the patient (either "assigned" or "waiting_for_doctor")
    assigned_specialist_id = None
    patient_status = "waiting_for_doctor"

    #if a specialist is found, assign the patient to that specialist and update the patient's status to "assigned".
    if specialist:
        assigned_specialist_id = specialist.id
        specialist.active_patients += 1
        patient_status = "assigned"

    # If no specialist is available, look for a lower priority patient who is currently assigned to a doctor in the same department and has a higher triage level than the incoming patient.
    # If such a patient is found, pause that patient's treatment, unassign them from their doctor, and assign the incoming patient to that doctor instead. The function returns the ID of the assigned specialist (if any) and the status of the patient (either "assigned" or "waiting_for_doctor").
    else:

        #query to find a lower priority patient who is currently assigned to a doctor in the same department and has a higher triage level than the incoming patient.
        lower_priority_patient = (
            db.query(Patient)
            .filter(
                Patient.status == "assigned",
                Patient.triage_level > triage_level,
                Patient.department_needed == department_needed
            )
            .order_by(Patient.triage_level.desc())
            .first()
        )

        #if such a patient is found, pause that patient's treatment, unassign them from their doctor, and assign the incoming patient to that doctor instead. The function returns the ID of the assigned specialist (if any) and the status of the patient (either "assigned" or "waiting_for_doctor").
        if lower_priority_patient:

            #query to find the specialist assigned to the lower priority patient
            specialist = (
                db.query(Doctor)
                .filter(
                    Doctor.id ==
                    lower_priority_patient.assigned_doctor_id
                )
                .first()
            )

            gp = get_available_gp(db)
            if gp:
                 lower_priority_patient.status = "awaiting_specialist"
                 lower_priority_patient.assigned_doctor_id = gp.id
                 gp.active_patients += 1
            else:
                 lower_priority_patient.status = "awaiting_specialist"
                 lower_priority_patient.assigned_doctor_id = None

            assigned_specialist_id = specialist.id
            patient_status = "assigned"

    return {
        "assigned_specialist_id": assigned_specialist_id,
        "patient_status": patient_status
    }

'''this function is a helper function to get an available GP doctor for patient intake.'''
def get_available_gp(db: Session):
    return (
        #query to find an available GP doctor in the DB
        db.query(Doctor)
        .filter(
            Doctor.department == "GP",
            Doctor.active_patients < Doctor.max_patient_limit
        )
        .order_by(Doctor.active_patients.asc())
        .first()
    )