import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

describe('Scaffold React + Vite + PWA', () => {
    it('renderiza la interfaz de corrección inicial (Hito v0.5-001)', () => {
        render(<App />)

        // Verificamos que tu componente base se dibuja correctamente 
        const titulo = screen.getByText('Captura de Examen')
        expect(titulo).toBeInTheDocument()
    })
})