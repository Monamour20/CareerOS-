from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.career_profile import CareerProfileRecord


class EducationRecord(Base):
    __tablename__ = "education"

    id: Mapped[int] = mapped_column(primary_key=True)
    career_profile_id: Mapped[int] = mapped_column(
        ForeignKey("career_profiles.id", ondelete="CASCADE"), index=True
    )
    institution: Mapped[str | None] = mapped_column(String(255))
    degree: Mapped[str | None] = mapped_column(String(255))
    field_of_study: Mapped[str | None] = mapped_column(String(255))
    start_date: Mapped[str | None] = mapped_column(String(64))
    end_date: Mapped[str | None] = mapped_column(String(64))
    sort_order: Mapped[int] = mapped_column(default=0)

    career_profile: Mapped[CareerProfileRecord] = relationship(back_populates="education")
    details: Mapped[list[EducationDetailRecord]] = relationship(
        back_populates="education", cascade="all, delete-orphan"
    )


class EducationDetailRecord(Base):
    __tablename__ = "education_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    education_id: Mapped[int] = mapped_column(ForeignKey("education.id", ondelete="CASCADE"))
    detail: Mapped[str] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(default=0)

    education: Mapped[EducationRecord] = relationship(back_populates="details")
