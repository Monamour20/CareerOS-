from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.job_skill import JobSkillRecord


class JobRecord(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)

    external_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source: Mapped[str] = mapped_column(String(64), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)

    remote: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    employment_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    seniority: Mapped[str | None] = mapped_column(String(64), nullable=True)

    description: Mapped[str] = mapped_column(Text, nullable=False)

    application_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    salary_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    salary_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    currency: Mapped[str | None] = mapped_column(String(16), nullable=True)

    posted_at: Mapped[str | None] = mapped_column(String(64), nullable=True)
    expires_at: Mapped[str | None] = mapped_column(String(64), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    skills: Mapped[list[JobSkillRecord]] = relationship(
        back_populates="job",
        cascade="all, delete-orphan",
        order_by="JobSkillRecord.id",
    )