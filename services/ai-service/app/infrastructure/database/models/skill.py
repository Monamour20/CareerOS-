from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.career_profile import CareerProfileRecord


class SkillRecord(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    career_profile_id: Mapped[int] = mapped_column(
        ForeignKey("career_profiles.id", ondelete="CASCADE"), index=True
    )
    category: Mapped[str] = mapped_column(String(64), index=True)
    name: Mapped[str] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(default=0)

    career_profile: Mapped[CareerProfileRecord] = relationship(back_populates="skills")
