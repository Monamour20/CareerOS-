from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.career_profile import CareerProfileRecord


class CareerPreferenceRecord(Base):
    __tablename__ = "career_preferences"

    id: Mapped[int] = mapped_column(primary_key=True)
    career_profile_id: Mapped[int] = mapped_column(
        ForeignKey("career_profiles.id", ondelete="CASCADE"), unique=True
    )
    seniority: Mapped[str | None] = mapped_column(String(128))

    career_profile: Mapped[CareerProfileRecord] = relationship(back_populates="career_preference")
    items: Mapped[list[CareerPreferenceItemRecord]] = relationship(
        back_populates="career_preference", cascade="all, delete-orphan"
    )


class CareerPreferenceItemRecord(Base):
    __tablename__ = "career_preference_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    career_preference_id: Mapped[int] = mapped_column(
        ForeignKey("career_preferences.id", ondelete="CASCADE"), index=True
    )
    category: Mapped[str] = mapped_column(String(64), index=True)
    value: Mapped[str] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(default=0)

    career_preference: Mapped[CareerPreferenceRecord] = relationship(back_populates="items")
