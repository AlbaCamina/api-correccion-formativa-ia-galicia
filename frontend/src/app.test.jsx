import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

describe('Scaffold React + Vite + PWA', () => {
    it('renderiza la interfaz de corrección inicial (Hito v0.5-001)', () => {
        render(<App />)

        // Verificamos que tu componente base se dibuja correctamente en pantalla
        const titulo = screen.getByText('Panel de Trabajo')
        expect(titulo).toBeInTheDocument()
    })
})