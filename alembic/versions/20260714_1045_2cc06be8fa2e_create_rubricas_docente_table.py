"""create rubricas_docente table

Revision ID: 2cc06be8fa2e
Revises: a43a0d927d6d
Create Date: 2026-07-14 10:45:00.000000+02:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cc06be8fa2e'
down_revision: Union[str, None] = 'a43a0d927d6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('rubricas_docente',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('profesor_id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.Column('criterios', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['profesor_id'], ['profesores.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rubricas_docente_id'), 'rubricas_docente', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_rubricas_docente_id'), table_name='rubricas_docente')
    op.drop_table('rubricas_docente')
