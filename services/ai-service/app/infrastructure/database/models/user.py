from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.auth_session import AuthSessionRecord
    from app.infrastructure.database.models.career_profile import CareerProfileRecord


class UserRecord(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str | None] = mapped_column(String(320), unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String(255))
    password_hash: Mapped[str | None] = mapped_column(String(512))
    account_type: Mapped[str | None] = mapped_column(String(64))
    career_status: Mapped[str | None] = mapped_column(String(64))
    preferred_work_mode: Mapped[str | None] = mapped_column(String(64))
    career_goals: Mapped[str | None] = mapped_column(String(2000))
    onboarding_completed: Mapped[bool] = mapped_column(default=False, server_default="false")
    resume_creation_requested: Mapped[bool] = mapped_column(default=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    career_profile: Mapped[CareerProfileRecord | None] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    sessions: Mapped[list[AuthSessionRecord]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
