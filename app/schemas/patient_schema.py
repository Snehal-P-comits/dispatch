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

from pydantic import BaseModel, Field

#Schema for validating incoming data when creating a new patient
class PatientCreate(BaseModel):
    patient_name: str
    department_needed: str
    triage_level: int = Field(..., gt=0)

#Schema for validating incoming data when updating an existing patient
class PatientResponse(BaseModel):
    id: int
    patient_name: str
    department_needed: str
    assigned_doctor_id: int | None
    triage_level: int
    status: str

    #this is a special configuration for Pydantic models that allows them to be created from ORM objects
    # this means that if you have a SQLAlchemy model instance,
    # you can directly create a Pydantic model from it without needing to manually convert the fields
    class Config:
        from_attributes = True