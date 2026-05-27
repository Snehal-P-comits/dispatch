'''This file defines how doctors are stored in the database.

How things translate from Python to the database:
| Python    | Database |
| --------- | -------- |
| Class     | Table    |
| Object    | Row      |
| Attribute | Column   |

'''

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
# Importing the Base class from the database module to create a new table for doctors.
from app.database.base import Base

#table for doctors
class Doctor(Base):
    __tablename__ = "doctors" #name of the table in the database

    # id is the primary key and is auto-incremented
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    # doctor_name is a string and cannot be null
    doctor_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    # department is a string and cannot be null
    department: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    # active_patients is an integer that keeps track of how many patients are currently assigned to the doctor.
    # It defaults to 0.
    active_patients: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    # max_patient_limit is an integer that defines the maximum number of patients a doctor can have at a time. 
    # It defaults to 3.
    max_patient_limit: Mapped[int] = mapped_column(
        Integer,
        default=3
    )

'''
So the table would look like this:
# +----+--------------+--------------+------------------+-------------------+
# | id | doctor_name  | department   | active_patients | max_patient_limit |
# +----+--------------+--------------+------------------+-------------------+
# | 1  | Dr. SPOP     | Cardiology   |        1         |         3         |
# +----+--------------+--------------+------------------+-------------------+
'''