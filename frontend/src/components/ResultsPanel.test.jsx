import { render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import ResultsPanel from './ResultsPanel';

const completedEvaluation = {
    resultado_ia: {
        transcription: 'El alumno relaciona el mito de la caverna con la educación.',
        rubricBreakdown: [
            {
                criterio_codigo: 'FILO-B2.3',
                competencias_clave: ['CCL', 'CC'],
                category: 'Comprensión conceptual',
                score: 8,
                maxScore: 10,
                peso: 100,
                nivel_logro: 4,
                reasoning: 'Explica correctamente la idea principal.',
            },
        ],
        visualMarkers: [
            {
                type: 'MEJORA',
                message: 'Revisar la conclusión final.',
            },
        ],
        qualitativeAnalysis: {
            strengths: ['Relaciona correctamente las ideas principales.'],
            improvementNeeds: {
                immediate: ['Explicar mejor la relación con la política.'],
                mediumLongTerm: ['Practicar redacción filosófica formal.'],
            },
            teacherSummary: 'Muestra una comprensión sólida del contenido.',
        },
        calificacion_numerica: 8,
        calificacion_cualitativa: 'NT',
        siguiente_paso_accionable: 'Reescribe la conclusión con un ejemplo.',
        confidence_score: 0.92,
        etapa: 'ESO',
    },
};

const jsonResponse = (body, status = 200) => ({
    ok: status >= 200 && status < 300,
    status,
    json: vi.fn().mockResolvedValue(body),
});

describe('ResultsPanel - [v0.5.1-002] [D-024]', () => {
    let fetchMock;

    beforeEach(() => {
        fetchMock = vi.fn();
        vi.stubGlobal('fetch', fetchMock);
    });

    afterEach(() => {
        vi.unstubAllGlobals();
    });

    it('muestra el estado de análisis mientras la evaluación no está disponible', () => {
        fetchMock.mockResolvedValue(jsonResponse({}, 404));

        render(<ResultsPanel submissionId="submission-1" onReset={vi.fn()} />);

        expect(screen.getByText('Analizando con IA...')).toBeInTheDocument();
        expect(
            screen.getByText(/El motor multimodal está leyendo y evaluando/i)
        ).toBeInTheDocument();
    });

    it('renderiza todos los bloques principales de EvaluacionIA', async () => {
        fetchMock.mockResolvedValue(jsonResponse(completedEvaluation));

        render(<ResultsPanel submissionId="submission-1" onReset={vi.fn()} />);

        expect(
            await screen.findByText('Resultados de la Evaluación')
        ).toBeInTheDocument();

        expect(
            screen.getByText(
                'El alumno relaciona el mito de la caverna con la educación.'
            )
        ).toBeInTheDocument();
        expect(screen.getByText('Comprensión conceptual')).toBeInTheDocument();
        expect(screen.getByText('8 / 10')).toBeInTheDocument();
        expect(
            screen.getByText('Código: FILO-B2.3 · Competencias: CCL, CC')
        ).toBeInTheDocument();
        expect(
            screen.getByText('Explica correctamente la idea principal.')
        ).toBeInTheDocument();
        expect(
            screen.getByText('Relaciona correctamente las ideas principales.')
        ).toBeInTheDocument();
        expect(
            screen.getByText('Explicar mejor la relación con la política.')
        ).toBeInTheDocument();
        expect(
            screen.getByText('Practicar redacción filosófica formal.')
        ).toBeInTheDocument();
        expect(
            screen.getByText(/MEJORA.*Revisar la conclusión final\./)
        ).toBeInTheDocument();
        expect(
            screen.getByText(/Se detectaron 1 observación visual/i)
        ).toBeInTheDocument();
        expect(
            screen.getByText('Reescribe la conclusión con un ejemplo.')
        ).toBeInTheDocument();
    });

    it('muestra un error gestionado ante un error HTTP', async () => {
        fetchMock.mockResolvedValue(
            jsonResponse({ detail: 'La evaluación no está disponible.' }, 500)
        );

        render(<ResultsPanel submissionId="submission-1" onReset={vi.fn()} />);

        expect(
            await screen.findByText('Error al obtener resultados')
        ).toBeInTheDocument();
        expect(
            screen.getByText('La evaluación no está disponible.')
        ).toBeInTheDocument();
    });
});
