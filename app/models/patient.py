'''This file defines how patients are stored in the database.

How things translate from Python to the database:
| Python    | Database |
| --------- | -------- |
| Class     | Table    |
| Object    | Row      |
| Attribute | Column   |

'''

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
# Importing the Base class from the database module to create a new table for doctors.
from app.database.base import Base

#table for patients
class Patient(Base):
    __tablename__ = "patients" #name of the table in the database

    # id is the primary key and is auto-incremented
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    # patient_name is a string and cannot be null
    patient_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    # department_needed is a string and cannot be null
    department_needed: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    # assigned_doctor_id is an integer that references the id of the doctor assigned to the patient.
    # It can be null if no doctor is assigned yet.
    assigned_doctor_id: Mapped[int | None] = mapped_column(
        ForeignKey("doctors.id"),
        nullable=True
    )

    # triage_level is a number that indicates the severity of the patient's condition.
    # A lower number indicates a more severe condition, and a higher number indicates a less severe condition.
    # For example, a patient with a triage level of 1 would be in critical condition and require immediate attention,
    # while a patient with a triage level of 5 would be in stable condition and could wait longer for treatment.
    # triage_level is an integer and cannot be null
    triage_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # status is a string with a default value of "waiting_for_doctor"
    status: Mapped[str] = mapped_column(
        String,
        default="waiting_for_doctor"
    )

'''So the table would look like this:
# +----+---------------+---------------------+--------------------+---------------+----------------------+
# | id | patient_name  | department_needed   | assigned_doctor_id | triage_level  | status               |
# +----+---------------+---------------------+--------------------+---------------+----------------------+
# | 1  | Ayrus         | Cardiology          |         1          |       1       | assigned             |
# +----+---------------+---------------------+--------------------+---------------+----------------------+
Nice
'''