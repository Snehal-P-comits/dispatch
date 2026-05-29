'''
schema != model
| Models             | Schemas                     |
| ------------------ | --------------------------- |
| Database structure | Request/response validation |
| SQLAlchemy         | Pydantic                    |
| Talks to DB        | Talks to API users          |

this file defines the Pydantic schemas for the IdleQueue model, 
which are used for validating and serializing data in API requests and responses.
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