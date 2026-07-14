"""create marcos_evaluacion table

Revision ID: a43a0d927d6d
Revises: fed94eea19e8
Create Date: 2026-07-14 10:35:00.000000+02:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a43a0d927d6d'
down_revision: Union[str, None] = 'fed94eea19e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('marcos_evaluacion',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.Column('asignatura', sa.String(length=100), nullable=False),
    sa.Column('curso', sa.String(length=100), nullable=False),
    sa.Column('estado_activo', sa.Boolean(), nullable=False, server_default=sa.text('true')),
    sa.Column('rubrica_completa', sa.JSON(), nullable=False),
    sa.Column('ultima_verificacion_manual', sa.Date(), nullable=True),
    sa.Column('fuente_legislativa_url', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_marcos_evaluacion_id'), 'marcos_evaluacion', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_marcos_evaluacion_id'), table_name='marcos_evaluacion')
    op.drop_table('marcos_evaluacion')
