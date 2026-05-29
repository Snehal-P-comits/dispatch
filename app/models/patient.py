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
    __tablename__ = "patients"

    # id is the primary key and is auto-incremented
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    # patient_name is a string and cannot be null
    # so what does Mapped[str] mean?
    # It means that the patient_name attribute is a string that is mapped to a column in the database.
    # The mapped_column function is used to define the column in the database
    patient_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    # issue is a string and cannot be null
    #raw patient complaint.
    #NOT medical diagnosis.
    issue: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    # diagnosis_notes is a string and can be null
    diagnosis_notes: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # department_needed is a string and can be null
    department_needed: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # assigned_doctor_id is an integer and can be null,
    # it is a foreign key that references the id column in the doctors table
    assigned_doctor_id: Mapped[int | None] = mapped_column(
        ForeignKey("doctors.id"),
        nullable=True
    )

    # triage_level is a number that indicates the severity of the patient's condition.
    # It can be null if the patient has not been assessed yet.
    triage_level: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    # status is a string with a default value of "awaiting_assessment"
    status: Mapped[str] = mapped_column(
        String,
        default="awaiting_assessment"
    )


'''So the table would look like this:
# +----+---------------+----------------------------+-------------------+---------------------+--------------------+---------------+----------------------+
# | id | patient_name  | issue                      | diagnosis_notes   | department_needed   | assigned_doctor_id | triage_level  | status               |
# +----+---------------+----------------------------+-------------------+---------------------+--------------------+---------------+----------------------+
# | 1  | Snehal        | Chest pain                 | Possible cardiac  | Cardiology          |         2          |       1       | assigned             |
# | 2  | SPOP          | Migraine                   | NULL              | NULL                |       NULL         |     NULL      | awaiting_assessment  |
# +----+---------------+----------------------------+-------------------+---------------------+--------------------+---------------+----------------------+
'''