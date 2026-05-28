''' this module contains the business logic for patient intake, including doctor assignment and patient record creation. '''

#imprting the session class from SQLAlchemy to create a db session
from sqlalchemy.orm import Session

#importing the Doctor and Patient models to interact with the corresponding tables in the database
from app.models.doctor import Doctor
from app.models.patient import Patient

# This function handles the intake of a new patient,
# assigning them to an available GP and creating their patient record in the database.
def intake_patient(
    db: Session,# database session to interact with the database
    patient_name: str,# name of the patient being intaken
    issue: str #the issue that the patient has
):
    
    #query to find an available GP doctor in the DB
    available_gp = (
        db.query(Doctor)
        .filter(
            Doctor.department == "GP",# looking for doctors in the General Physician department
            Doctor.active_patients < Doctor.max_patient_limit # ensuring the doctor has not reached their maximum patient limit
        )
        .order_by(Doctor.active_patients.asc())# prioritizing doctors with fewer active patients to balance the workload
        .first()#returning the first value that matches the criteria
    )

    #the assigned gp's doctor id
    assigned_gp_id = None

    # If an available GP is found,
    # we assign the patient to that GP and increment the GP's active patient count.
    if available_gp:
        assigned_gp_id = available_gp.id
        available_gp.active_patients += 1
        # after determining the assigned GP patient record is created
        new_patient = Patient(
            patient_name=patient_name,
            issue=issue,
            assigned_doctor_id=assigned_gp_id,
            status="awaiting_assessment"
        )
    
    else:
        # If no GP is available, we create the patient record without an assigned doctor and set the status to "awaiting_gp_assignment".
        new_patient = Patient(
            patient_name=patient_name,
            issue=issue,
            status="awaiting_gp_assignment"
        )

    # the new patient record is added to the database session,
    db.add(new_patient)

    # committed to save it to the database
    db.commit()

    # refreshed to get any updated fields (like the auto-generated id).
    db.refresh(new_patient)

    #returing the patient object
    return new_patient