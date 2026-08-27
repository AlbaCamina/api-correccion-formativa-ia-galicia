import { describe, it, expect, vi, afterEach } from 'vitest';
import { cropHeader } from '../utils/imageCrop';

describe('imageCrop utility [Zero Data Retention]', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('recorta el 20% superior del folio para garantizar la eliminación de la cabecera PII (folio estándar 794x1123px)', () => {
    // Arrange: Simular resolución A4 escaneada típica (794x1123px)
    const originalWidth = 794;
    const originalHeight = 1123;
    const topCropRatio = 0.20;
    
    // Matemática esperada: 1123 * 0.20 = 224.6 (se trunca a 224px)
    // Alto resultante esperado: 1123 - 224 = 899px
    const expectedHeight = 899;
    const expectedCropY = 224;

    // Mocks: Simular Canvas API ya que no tenemos DOM real en Vitest estándar
    const mockContext = {
      drawImage: vi.fn()
    };
    
    const mockCanvas = {
      width: 0,
      height: 0,
      getContext: vi.fn(() => mockContext)
    };

    // Espiar la creación de elementos DOM
    const createElementSpy = vi.spyOn(document, 'createElement').mockReturnValue(mockCanvas);
    const mockSourceImage = {}; // Mock genérico de la imagen fuente

    // Act
    const resultCanvas = cropHeader(mockSourceImage, originalWidth, originalHeight, topCropRatio);

    // Assert: Comprobar dimensiones del nuevo lienzo
    expect(createElementSpy).toHaveBeenCalledWith('canvas');
    expect(resultCanvas.width).toBe(originalWidth);
    expect(resultCanvas.height).toBe(expectedHeight); // 899px como define el criterio de aceptación

    // Assert: Comprobar coordenadas de recorte en la llamada a drawImage
    // drawImage(source, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight)
    expect(mockContext.drawImage).toHaveBeenCalledWith(
      mockSourceImage,
      0, expectedCropY, originalWidth, expectedHeight, // Origen de la fuente desplazado hacia abajo
      0, 0, originalWidth, expectedHeight // Destino anclado en 0,0
    );
  });

  it('verifica la proporcionalidad con ratio personalizado (0.25)', () => {
    const originalWidth = 1000;
    const originalHeight = 1000;
    const topCropRatio = 0.25;
    
    // Matemática esperada: 1000 * 0.25 = 250px recortados. Alto restante: 750px
    const expectedHeight = 750;

    const mockContext = { drawImage: vi.fn() };
    const mockCanvas = { width: 0, height: 0, getContext: vi.fn(() => mockContext) };
    vi.spyOn(document, 'createElement').mockReturnValue(mockCanvas);

    const resultCanvas = cropHeader({}, originalWidth, originalHeight, topCropRatio);

    expect(resultCanvas.height).toBe(expectedHeight);
    
    // Conservación de píxeles: cabecera.alto (250) + cuerpo.alto (750) === original.alto (1000)
    expect(250 + resultCanvas.height).toBe(originalHeight);
  });

  it('caso borde ratio = 0.0: cuerpo === imagen completa', () => {
    const originalWidth = 500;
    const originalHeight = 500;
    const topCropRatio = 0.0;
    
    const mockContext = { drawImage: vi.fn() };
    const mockCanvas = { width: 0, height: 0, getContext: vi.fn(() => mockContext) };
    vi.spyOn(document, 'createElement').mockReturnValue(mockCanvas);

    const resultCanvas = cropHeader({}, originalWidth, originalHeight, topCropRatio);

    expect(resultCanvas.height).toBe(originalHeight);
  });

  it('caso borde ratio = 1.0: cuerpo vacío (0 height)', () => {
    const originalWidth = 500;
    const originalHeight = 500;
    const topCropRatio = 1.0;
    
    const mockContext = { drawImage: vi.fn() };
    const mockCanvas = { width: 0, height: 0, getContext: vi.fn(() => mockContext) };
    vi.spyOn(document, 'createElement').mockReturnValue(mockCanvas);

    const resultCanvas = cropHeader({}, originalWidth, originalHeight, topCropRatio);

    expect(resultCanvas.height).toBe(0);
  });

  it('lanza un error si no se proporciona una imagen fuente (Fail Fast)', () => {
    expect(() => cropHeader(null, 794, 1123)).toThrow('sourceImage is required');
  });
});
