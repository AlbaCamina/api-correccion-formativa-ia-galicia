import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import CameraCapture from './CameraCapture';

describe('CameraCapture Component - [v0.5-002]', () => {
  it('renderiza correctamente los controles del modo dual inicial', () => {
    render(<CameraCapture />);
    
    // Verifica que el título esté presente
    expect(screen.getByText('Captura de Examen')).toBeInTheDocument();
    
    // Verifica que el botón de cámara exista
    const btnCamara = screen.getByText('📸 Abrir Cámara');
    expect(btnCamara).toBeInTheDocument();
    
    // Verifica que el input de subida de archivo exista
    const labelSubida = screen.getByText(/Subir Archivo/i);
    expect(labelSubida).toBeInTheDocument();
  });

  it('el input de archivo acepta imágenes (modo fotocopiadora)', () => {
    render(<CameraCapture />);
    
    // Buscar por rol genérico ya que el input está oculto por el label
    // No podemos interactuar directamente con el canvas en jsdom porque no tiene 
    // implementación real de 2d context en el entorno de consola puro,
    // pero verificamos que la barrera de entrada está lista.
    const fileInput = screen.getByLabelText(/Subir Archivo/i);
    expect(fileInput).toHaveAttribute('type', 'file');
    expect(fileInput).toHaveAttribute('accept', 'image/*');
  });
});
