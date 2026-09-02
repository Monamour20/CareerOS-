from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.job import JobRecord


class JobSkillRecord(Base):
    __tablename__ = "job_skills"

    id: Mapped[int] = mapped_column(primary_key=True)

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    job: Mapped[JobRecord] = relationship(
        back_populates="skills",
    )