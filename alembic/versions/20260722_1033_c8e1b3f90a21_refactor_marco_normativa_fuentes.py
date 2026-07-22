"""refactor(marco): sustituir fuente_legislativa_url por normativa_fuentes (JSON list)

Motivación: Blindaje de extensibilidad multi-autonómica [D-033].
  - fuente_legislativa_url (VARCHAR simple) no soporta múltiples decretos por marco.
  - normativa_fuentes (JSON) acepta una lista de objetos:
      {tipo, numero, fecha, url, vigente_desde, vigente_hasta}
  - El valor existente en fuente_legislativa_url se migra como primer elemento de la lista.
  - ultima_verificacion_manual NO se toca (es meta-auditoría, no normativa).

Revision ID: c8e1b3f90a21
Revises: 1ff2479bc0f8
Create Date: 2026-07-22 10:33:00.000000+02:00
"""
from typing import Sequence, Union
import json

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = 'c8e1b3f90a21'
down_revision: Union[str, None] = '1ff2479bc0f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Añadir la nueva columna JSON (nullable para no romper filas existentes)
    op.add_column(
        'marcos_evaluacion',
        sa.Column('normativa_fuentes', sa.JSON(), nullable=True)
    )

    # 2. Migrar el dato existente de fuente_legislativa_url → normativa_fuentes
    #    Solo para las filas que tienen un valor no nulo en fuente_legislativa_url.
    conn = op.get_bind()
    rows = conn.execute(
        text("SELECT id, fuente_legislativa_url FROM marcos_evaluacion WHERE fuente_legislativa_url IS NOT NULL")
    ).fetchall()

    for row in rows:
        marco_id, url = row[0], row[1]
        fuentes = [
            {
                "tipo": "decreto",
                "numero": None,
                "fecha": None,
                "url": url,
                "vigente_desde": None,
                "vigente_hasta": None
            }
        ]
        conn.execute(
            text("UPDATE marcos_evaluacion SET normativa_fuentes = :fuentes WHERE id = :id"),
            {"fuentes": json.dumps(fuentes), "id": marco_id}
        )

    # 3. Eliminar la columna fuente_legislativa_url ya migrada
    op.drop_column('marcos_evaluacion', 'fuente_legislativa_url')


def downgrade() -> None:
    # 1. Recuperar la columna plana original
    op.add_column(
        'marcos_evaluacion',
        sa.Column('fuente_legislativa_url', sa.String(length=500), nullable=True)
    )

    # 2. Revertir: extraer la URL del primer elemento de normativa_fuentes (si existe)
    conn = op.get_bind()
    rows = conn.execute(
        text("SELECT id, normativa_fuentes FROM marcos_evaluacion WHERE normativa_fuentes IS NOT NULL")
    ).fetchall()

    for row in rows:
        marco_id, fuentes_raw = row[0], row[1]
        # normativa_fuentes puede llegar como string o como objeto según el driver
        if isinstance(fuentes_raw, str):
            fuentes = json.loads(fuentes_raw)
        else:
            fuentes = fuentes_raw

        url = None
        if isinstance(fuentes, list) and len(fuentes) > 0:
            url = fuentes[0].get("url")

        if url:
            conn.execute(
                text("UPDATE marcos_evaluacion SET fuente_legislativa_url = :url WHERE id = :id"),
                {"url": url, "id": marco_id}
            )

    # 3. Eliminar la nueva columna
    op.drop_column('marcos_evaluacion', 'normativa_fuentes')
