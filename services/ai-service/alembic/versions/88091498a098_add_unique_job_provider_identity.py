"""add unique job provider identity

Revision ID: 88091498a098
Revises: fe77207c75f5
Create Date: 2026-09-01 18:59:00.236743

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "88091498a098"
down_revision: Union[str, Sequence[str], None] = "fe77207c75f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "uq_jobs_source_external_id",
        "jobs",
        ["source", "external_id"],
        unique=True,
        postgresql_where="external_id IS NOT NULL",
    )


def downgrade() -> None:
    op.drop_index(
        "uq_jobs_source_external_id",
        table_name="jobs",
    )