from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.achievement import AchievementRecord
    from app.infrastructure.database.models.career_preference import CareerPreferenceRecord
    from app.infrastructure.database.models.certification import CertificationRecord
    from app.infrastructure.database.models.education import EducationRecord
    from app.infrastructure.database.models.experience import ExperienceRecord
    from app.infrastructure.database.models.project import ProjectRecord
    from app.infrastructure.database.models.skill import SkillRecord
    from app.infrastructure.database.models.user import UserRecord


class CareerProfileRecord(Base):
    __tablename__ = "career_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    phone: Mapped[str | None] = mapped_column(String(64))
    location: Mapped[str | None] = mapped_column(String(255))
    linkedin: Mapped[str | None] = mapped_column(String(500))
    github: Mapped[str | None] = mapped_column(String(500))
    summary: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped[UserRecord] = relationship(back_populates="career_profile")
    education: Mapped[list[EducationRecord]] = relationship(
        back_populates="career_profile", cascade="all, delete-orphan"
    )
    experience: Mapped[list[ExperienceRecord]] = relationship(
        back_populates="career_profile", cascade="all, delete-orphan"
    )
    skills: Mapped[list[SkillRecord]] = relationship(
        back_populates="career_profile", cascade="all, delete-orphan"
    )
    projects: Mapped[list[ProjectRecord]] = relationship(
        back_populates="career_profile", cascade="all, delete-orphan"
    )
    certifications: Mapped[list[CertificationRecord]] = relationship(
        back_populates="career_profile", cascade="all, delete-orphan"
    )
    achievements: Mapped[list[AchievementRecord]] = relationship(
        back_populates="career_profile", cascade="all, delete-orphan"
    )
    career_preference: Mapped[CareerPreferenceRecord | None] = relationship(
        back_populates="career_profile", cascade="all, delete-orphan", uselist=False
    )
