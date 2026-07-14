"""
Script de inicialización y carga de semillas (seeding) para la base de datos de api-correccion-formativa-ia-galicia.
Precarga el currículo oficial de Filosofía de 1º de Bachillerato según el Decreto 157/2022 de la Xunta de Galicia.
Incluye los metadatos de vigencia legislativa en cumplimiento del ADR [D-033].
"""
import os
import sys
from datetime import date
from sqlalchemy.orm import Session

# Asegurar que el directorio raíz está en el path para importaciones del backend
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.models.database import SessionLocal, engine, Base
from backend.models.marco import MarcoEvaluacion


def seed_database():
    print("Iniciando carga de semillas en la base de datos...")
    
    # Crear sesión de base de datos
    db: Session = SessionLocal()
    
    try:
        # Verificar si ya existe el marco oficial de Filosofía de Galicia
        existing_marco = db.query(MarcoEvaluacion).filter(
            MarcoEvaluacion.nombre == "Decreto 157/2022 - Currículo de Filosofía en Galicia",
            MarcoEvaluacion.curso == "1º Bachillerato"
        ).first()
        
        if existing_marco:
            print("El marco de evaluación de Filosofía para Galicia ya está precargado.")
            return

        # Estructura del currículo oficial según el Decreto 157/2022 de la Xunta de Galicia
        rubrica_completa_galicia = {
            "competencias_especificas": [
                {
                    "id": "CE1",
                    "nombre": "Identificación de problemas filosóficos",
                    "descripcion": "Identificar problemas filosóficos y debatir sobre ellos a través del análisis de textos e ideas filosóficas fundamentales, utilizando con propiedad el vocabulario técnico específico.",
                    "criterios_evaluacion": [
                        {
                            "id": "1.1",
                            "criterio": "Analizar textos filosóficos identificando sus tesis principales y la estructura de su argumentación.",
                            "descriptores_asociados": ["CCL2", "CPSAA4", "CC1"]
                        },
                        {
                            "id": "1.2",
                            "criterio": "Explicar conceptos filosóficos clave utilizando con rigor y propiedad el vocabulario técnico de la materia.",
                            "descriptores_asociados": ["CCL2", "CC1"]
                        }
                    ]
                },
                {
                    "id": "CE2",
                    "nombre": "Argumentación y razonamiento crítico",
                    "descripcion": "Argumentar con rigor conceptual, coherencia lógica y honestidad intelectual problemas éticos, políticos y del conocimiento humano, distinguiendo argumentos válidos de falacias.",
                    "criterios_evaluacion": [
                        {
                            "id": "2.1",
                            "criterio": "Elaborar de forma guiada disertaciones y análisis críticos estructurados, argumentando con lógica y evitando falacias.",
                            "descriptores_asociados": ["CCL1", "CCL5", "CPSAA1.2", "CC3"]
                        },
                        {
                            "id": "2.2",
                            "criterio": "Contrastar críticamente perspectivas filosóficas opuestas manifestando tolerancia e imparcialidad conceptual.",
                            "descriptores_asociados": ["CCL5", "CC1", "CC2"]
                        }
                    ]
                },
                {
                    "id": "CE3",
                    "nombre": "Acción moral y política",
                    "descripcion": "Analizar de forma crítica los fundamentos éticos y políticos del Estado social y democrático de derecho, comprendiendo la importancia de los derechos humanos y la equidad social.",
                    "criterios_evaluacion": [
                        {
                            "id": "3.1",
                            "criterio": "Evaluar la fundamentación de las normas morales y políticas confrontando teorías deontológicas, utilitaristas y de la virtud.",
                            "descriptores_asociados": ["CC1", "CC2", "CC3", "CE1"]
                        }
                    ]
                }
            ],
            "saberes_basicos": [
                {
                    "bloque": "Bloque 1: El saber filosófico y su historia",
                    "contenidos": [
                        "El origen de la filosofía y su diferencia con el mito y la ciencia.",
                        "Grandes preguntas e hitos de la historia de la filosofía occidental."
                    ]
                },
                {
                    "bloque": "Bloque 2: Conocimiento, verdad y ciencia",
                    "contenidos": [
                        "El problema del conocimiento: realismo, escepticismo y constructivismo.",
                        "El método científico, límites del saber científico y pseudociencias."
                    ]
                },
                {
                    "bloque": "Bloque 3: Acción moral y política",
                    "contenidos": [
                        "Fundamentos de la ética: el bien, el deber, la justicia y los derechos humanos.",
                        "Teorías sobre el origen de la sociedad, legitimidad política y formas de Estado."
                    ]
                }
            ]
        }

        # Crear instancia de MarcoEvaluacion con metadatos de vigencia [D-033]
        nuevo_marco = MarcoEvaluacion(
            nombre="Decreto 157/2022 - Currículo de Filosofía en Galicia",
            asignatura="Filosofía",
            curso="1º Bachillerato",
            estado_activo=True,
            rubrica_completa=rubrica_completa_galicia,
            ultima_verificacion_manual=date(2026, 7, 14),
            fuente_legislativa_url="https://www.xunta.gal/dog/Publicados/2022/20220603/AnuncioG0656-260522-0001_gl.html"
        )
        
        db.add(nuevo_marco)
        db.commit()
        print("¡Semilla cargada con éxito! Creado marco oficial de Filosofía para Galicia.")
        
    except Exception as e:
        db.rollback()
        print(f"Error al cargar las semillas: {str(e)}", file=sys.stderr)
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
