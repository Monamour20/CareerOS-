from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.career_profile import CareerProfileRecord


class ProjectRecord(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    career_profile_id: Mapped[int] = mapped_column(
        ForeignKey("career_profiles.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(default=0)

    career_profile: Mapped[CareerProfileRecord] = relationship(back_populates="projects")
    technologies: Mapped[list[ProjectTechnologyRecord]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    links: Mapped[list[ProjectLinkRecord]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class ProjectTechnologyRecord(Base):
    __tablename__ = "project_technologies"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    technology: Mapped[str] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(default=0)

    project: Mapped[ProjectRecord] = relationship(back_populates="technologies")


class ProjectLinkRecord(Base):
    __tablename__ = "project_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    url: Mapped[str] = mapped_column(String(500))
    sort_order: Mapped[int] = mapped_column(default=0)

    project: Mapped[ProjectRecord] = relationship(back_populates="links")
