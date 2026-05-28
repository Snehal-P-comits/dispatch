from pydantic import BaseModel


class DischargedPatientResponse(BaseModel):
    id: int
    patient_name: str
    issue: str
    diagnosis_notes: str | None
    department_needed: str | None
    assigned_doctor_id: int | None
    triage_level: int | None

    class Config:
        from_attributes = True