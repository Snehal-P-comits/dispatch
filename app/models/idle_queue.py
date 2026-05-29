'''This file defines how idle queue entries are stored in the database.

How things translate from Python to the database:
| Python    | Database |
| --------- | -------- |
| Class     | Table    |
| Object    | Row      |
| Attribute | Column   |

'''

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class IdleQueue(Base):
    __tablename__ = "idle_queue"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    required_department: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    queue_reason: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

'''
So the table would look like this:
# +----+------------+---------------------+------------------------+
# | id | patient_id | required_department | queue_reason           |
# +----+------------+---------------------+------------------------+
# | 1  | 42         | Cardiology          | specialist_unavailable |
# | 2  | 17         | Neurology           | preempted              |
# | 3  | 55         | NULL                | gp_unavailable         |
# +----+------------+---------------------+------------------------+
'''