"""add archivos_urls to submissions

Revision ID: 4a1b2c3d4e5f
Revises: 326ff2789e2e
Create Date: 2026-10-09 13:30:00.000000+02:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a1b2c3d4e5f'
down_revision: Union[str, None] = '326ff2789e2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('submissions', sa.Column('archivos_urls', sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column('submissions', 'archivos_urls')
