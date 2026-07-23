import unittest
from pydantic import ValidationError
from backend.models.evaluation import EvaluacionIA

class TestEvaluacionIA(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            "transcription": "El prisionero sale a la luz exterior y ve el sol que es la idea de Bien.",
            "rubricBreakdown": [
                {
                    "category": "Comprensión conceptual",
                    "score": 4.5,
                    "maxScore": 5.0,
                    "reasoning": "Muestra buen entendimiento del mito."
                }
            ],
            "visualMarkers": [],
            "qualitativeAnalysis": {
                "strengths": ["Buena comprensión conceptual del mito de la caverna."],
                "improvementNeeds": {
                    "immediate": ["Profundizar en la relación de la educación con la política."],
                    "mediumLongTerm": ["Trabajar la redacción filosófica formal."]
                },
                "teacherSummary": "Excelente respuesta en comprensión conceptual."
            },
            "calificacion_numerica": 8.0,
            "calificacion_cualitativa": "NT",
            "siguiente_paso_accionable": "Reescribe explicando por qué el filósofo debe gobernar la polis.",
            "confidence_score": 0.95,
            "etapa": "BACH"
        }

    def test_valid_evaluation(self):
        """Valida que un diccionario con los campos correctos se parsea exitosamente."""
        evaluation = EvaluacionIA(**self.valid_data)
        self.assertIsNone(evaluation.calificacion_cualitativa)
        self.assertEqual(evaluation.visualMarkers, [])

    def test_missing_required_field(self):
        """Valida que falta un campo obligatorio (ej. transcription) lanza ValidationError (422)."""
        invalid_data = self.valid_data.copy()
        del invalid_data["transcription"]
        with self.assertRaises(ValidationError):
            EvaluacionIA(**invalid_data)

    def test_missing_etapa_validation_error(self):
        """Valida que omitir la etapa lanza ValidationError (422), probando el breaking change D-041."""
        invalid_data = self.valid_data.copy()
        del invalid_data["etapa"]
        with self.assertRaises(ValidationError):
            EvaluacionIA(**invalid_data)

    def test_invalid_calificacion_cualitativa(self):
        """Valida que un valor fuera de la Literal permitida lanza ValidationError (422)."""
        invalid_data = self.valid_data.copy()
        invalid_data["calificacion_cualitativa"] = "APROBADO"  # Inválido, debe ser IN, SU, BE, NT, SB
        with self.assertRaises(ValidationError):
            EvaluacionIA(**invalid_data)

    def test_visual_markers_default(self):
        """Valida que omitir visualMarkers inicializa una lista vacía por defecto para texto plano."""
        data_no_markers = self.valid_data.copy()
        if "visualMarkers" in data_no_markers:
            del data_no_markers["visualMarkers"]
        evaluation = EvaluacionIA(**data_no_markers)
        self.assertEqual(evaluation.visualMarkers, [])

if __name__ == "__main__":
    unittest.main()
