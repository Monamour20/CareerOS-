"""create jobs tables

Revision ID: fe77207c75f5
Revises: 20260821_0003
Create Date: 2026-08-31

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fe77207c75f5"
down_revision: Union[str, Sequence[str], None] = "20260821_0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "external_id",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "source",
            sa.String(length=64),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "company",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "location",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "remote",
            sa.Boolean(),
            server_default="false",
            nullable=False,
        ),
        sa.Column(
            "employment_type",
            sa.String(length=64),
            nullable=True,
        ),
        sa.Column(
            "seniority",
            sa.String(length=64),
            nullable=True,
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "application_url",
            sa.String(length=1000),
            nullable=True,
        ),
        sa.Column(
            "salary_min",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "salary_max",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "currency",
            sa.String(length=16),
            nullable=True,
        ),
        sa.Column(
            "posted_at",
            sa.String(length=64),
            nullable=True,
        ),
        sa.Column(
            "expires_at",
            sa.String(length=64),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_jobs_external_id",
        "jobs",
        ["external_id"],
        unique=False,
    )

    op.create_index(
        "uq_jobs_source_external_id",
        "jobs",
        ["source", "external_id"],
        unique=True,
        postgresql_where=sa.text(
            "external_id IS NOT NULL"
        ),
    )

    op.create_index(
        "ix_jobs_source",
        "jobs",
        ["source"],
        unique=False,
    )

    op.create_index(
        "ix_jobs_title",
        "jobs",
        ["title"],
        unique=False,
    )

    op.create_index(
        "ix_jobs_company",
        "jobs",
        ["company"],
        unique=False,
    )

    op.create_table(
        "job_skills",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "job_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "required",
            sa.Boolean(),
            server_default="true",
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["job_id"],
            ["jobs.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_job_skills_job_id",
        "job_skills",
        ["job_id"],
        unique=False,
    )

    op.create_index(
        "ix_job_skills_name",
        "job_skills",
        ["name"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_job_skills_name",
        table_name="job_skills",
    )

    op.drop_index(
        "ix_job_skills_job_id",
        table_name="job_skills",
    )

    op.drop_table("job_skills")

    op.drop_index(
        "ix_jobs_company",
        table_name="jobs",
    )

    op.drop_index(
        "ix_jobs_title",
        table_name="jobs",
    )

    op.drop_index(
        "ix_jobs_source",
        table_name="jobs",
    )

    op.drop_index(
        "uq_jobs_source_external_id",
        table_name="jobs",
    )

    op.drop_index(
        "ix_jobs_external_id",
        table_name="jobs",
    )

    op.drop_table("jobs")