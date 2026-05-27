'''
schema != model
| Models             | Schemas                     |
| ------------------ | --------------------------- |
| Database structure | Request/response validation |
| SQLAlchemy         | Pydantic                    |
| Talks to DB        | Talks to API users          |

this file defines the Pydantic schemas for the Doctor model, 
which are used for validating and serializing data in API requests and responses.
'''

from pydantic import BaseModel, Field

#Schema for validating incoming data when creating a new doctor
class DoctorCreate(BaseModel):
    doctor_name: str
    department: str
    max_patient_limit: int = Field(..., gt=0)

#Schema for validating incoming data when updating an existing doctor
class DoctorResponse(BaseModel):
    id: int
    doctor_name: str
    department: str
    active_patients: int
    max_patient_limit: int = Field(..., gt=0)
    #what is feild()?
    #Field is a function from Pydantic that allows you to specify additional validation rules and metadata for a model field.
    #In this case, Field(..., gt=0) means that the max_patient_limit must be greater than 0,
    #and the ... indicates that this field is required.

    #this is a special configuration for Pydantic models that allows them to be created from ORM objects
    # this means that if you have a SQLAlchemy model instance,
    # you can directly create a Pydantic model from it without needing to manually convert the fields
    class Config:
        from_attributes = True