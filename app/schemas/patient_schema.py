'''
schema != model
| Models             | Schemas                     |
| ------------------ | --------------------------- |
| Database structure | Request/response validation |
| SQLAlchemy         | Pydantic                    |
| Talks to DB        | Talks to API users          |

this file defines the Pydantic schemas for the Patient model, 
which are used for validating and serializing data in API requests and responses.
'''

from pydantic import BaseModel, Field, model_validator

# PATIENT INTAKE SCHEMA
# Used when patient first enters the system
class PatientCreate(BaseModel):
    patient_name: str
    issue: str

# GP ASSESSMENT SCHEMA
# Used by General Physician after assessment
class GPAssessment(BaseModel):
    diagnosis_notes: str
    requires_specialist: bool
    department_needed: str | None = None
    triage_level: int | None = Field(
        default=None,
        ge=1,
        le=5
)

    @model_validator(mode="after")
    def validate_specialist_fields(self):
        if self.requires_specialist:
            if self.department_needed is None:
                raise ValueError(
                    "department_needed is required when requires_specialist=True"
                )

            if self.triage_level is None:
                raise ValueError(
                    "triage_level is required when requires_specialist=True"
                )

        return self


# RESPONSE SCHEMA
# Returned by API responses
class PatientResponse(BaseModel):
    id: int
    patient_name: str
    issue: str
    diagnosis_notes: str | None #can be null if not assessed yet
    department_needed: str | None #can be null if not assessed yet
    assigned_doctor_id: int | None #can be null if not assigned yet
    triage_level: int | None #can be null if not assessed yet
    status: str

    #this is a special configuration for Pydantic models that allows them to be created from ORM objects
    # this means that if you have a SQLAlchemy model instance,
    # you can directly create a Pydantic model from it without needing to manually convert the fields
    class Config:
        from_attributes = True