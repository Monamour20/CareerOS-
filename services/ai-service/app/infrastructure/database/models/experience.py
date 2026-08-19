from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.career_profile import CareerProfileRecord


class ExperienceRecord(Base):
    __tablename__ = "experience"

    id: Mapped[int] = mapped_column(primary_key=True)
    career_profile_id: Mapped[int] = mapped_column(
        ForeignKey("career_profiles.id", ondelete="CASCADE"), index=True
    )
    company: Mapped[str | None] = mapped_column(String(255))
    title: Mapped[str | None] = mapped_column(String(255))
    location: Mapped[str | None] = mapped_column(String(255))
    start_date: Mapped[str | None] = mapped_column(String(64))
    end_date: Mapped[str | None] = mapped_column(String(64))
    sort_order: Mapped[int] = mapped_column(default=0)

    career_profile: Mapped[CareerProfileRecord] = relationship(back_populates="experience")
    responsibilities: Mapped[list[ExperienceResponsibilityRecord]] = relationship(
        back_populates="experience", cascade="all, delete-orphan"
    )
    technologies: Mapped[list[ExperienceTechnologyRecord]] = relationship(
        back_populates="experience", cascade="all, delete-orphan"
    )


class ExperienceResponsibilityRecord(Base):
    __tablename__ = "experience_responsibilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    experience_id: Mapped[int] = mapped_column(ForeignKey("experience.id", ondelete="CASCADE"))
    responsibility: Mapped[str] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(default=0)

    experience: Mapped[ExperienceRecord] = relationship(back_populates="responsibilities")


class ExperienceTechnologyRecord(Base):
    __tablename__ = "experience_technologies"

    id: Mapped[int] = mapped_column(primary_key=True)
    experience_id: Mapped[int] = mapped_column(ForeignKey("experience.id", ondelete="CASCADE"))
    technology: Mapped[str] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(default=0)

    experience: Mapped[ExperienceRecord] = relationship(back_populates="technologies")
