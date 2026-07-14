"""create submissions, evaluaciones, changelog tables

Revision ID: 1f3dfc633a20
Revises: 2cc06be8fa2e
Create Date: 2026-07-14 11:06:00.000000+02:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f3dfc633a20'
down_revision: Union[str, None] = '2cc06be8fa2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Crear tabla submissions
    op.create_table('submissions',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('profesor_id', sa.Integer(), nullable=False),
    sa.Column('marco_id', sa.Integer(), nullable=True),
    sa.Column('rubrica_id', sa.Integer(), nullable=False),
    sa.Column('alumno_id', sa.String(length=100), nullable=True),
    sa.Column('adaptaciones_alumno', sa.JSON(), nullable=True),
    sa.Column('estado', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['profesor_id'], ['profesores.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['marco_id'], ['marcos_evaluacion.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['rubrica_id'], ['rubricas_docente.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_submissions_id'), 'submissions', ['id'], unique=False)

    # 2. Crear tabla evaluaciones
    op.create_table('evaluaciones',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('submission_id', sa.String(length=36), nullable=False),
    sa.Column('resultado_ia', sa.JSON(), nullable=False),
    sa.Column('nota_final', sa.Float(), nullable=True),
    sa.Column('aprobado_por_profesor', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['submission_id'], ['submissions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_evaluaciones_id'), 'evaluaciones', ['id'], unique=False)

    # 3. Crear tabla changelog
    op.create_table('changelog',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('submission_id', sa.String(length=36), nullable=False),
    sa.Column('accion', sa.String(length=255), nullable=False),
    sa.Column('actor', sa.String(length=100), nullable=False),
    sa.Column('datos_anteriores', sa.JSON(), nullable=True),
    sa.Column('datos_nuevos', sa.JSON(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['submission_id'], ['submissions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_changelog_id'), 'changelog', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_changelog_id'), table_name='changelog')
    op.drop_table('changelog')
    op.drop_index(op.f('ix_evaluaciones_id'), table_name='evaluaciones')
    op.drop_table('evaluaciones')
    op.drop_index(op.f('ix_submissions_id'), table_name='submissions')
    op.drop_table('submissions')
