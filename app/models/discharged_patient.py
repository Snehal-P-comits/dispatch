'''This file defines how discharged patients are stored in the database.

How things translate from Python to the database:
| Python    | Database |
| --------- | -------- |
| Class     | Table    |
| Object    | Row      |
| Attribute | Column   |

'''

# Importing necessary modules and classes to define the DischargedPatient model and interact with the database.
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

# Importing the Base class from the database module to create a new table for discharged patients.
from app.database.base import Base

# The DischargedPatient class defines the structure of the discharged_patients table in the database
class DischargedPatient(Base):
    __tablename__ = "discharged_patients" # name of the table in the database

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

    # issue is a string and cannot be null
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
        Integer,
        nullable=True
    )

    # triage_level is an integer and can be null
    triage_level: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )




'''

Nice
so this table would look like this:

# +----+---------------+----------------------------+-------------------+---------------------+--------------------+---------------+
# | id | patient_name  | issue                      | diagnosis_notes   | department_needed   | assigned_doctor_id | triage_level |
# +----+---------------+----------------------------+-------------------+---------------------+--------------------+---------------+
# | 1  | Rahul         | Chest pain                 | Cardiac emergency | Cardiology          |         2          |       1       |
# +----+---------------+----------------------------+-------------------+---------------------+--------------------+---------------+

'''