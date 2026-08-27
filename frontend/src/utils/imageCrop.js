/**
 * imageCrop.js
 * 
 * Utilidad de lógica pura para el recorte de imágenes (Privacy Redaction - Zero Data Retention).
 * Toma un elemento gráfico y recorta un porcentaje de la parte superior (cabecera).
 * 
 * [D-034] - Client-Side Redaction: Garantiza que el nombre del alumno no viaja al backend.
 */

/**
 * Recorta la parte superior de un lienzo de imagen por un ratio dado.
 * @param {HTMLCanvasElement|HTMLImageElement|ImageBitmap} sourceImage - La imagen original.
 * @param {number} originalWidth - Ancho original en píxeles.
 * @param {number} originalHeight - Alto original en píxeles.
 * @param {number} topCropRatio - El porcentaje a recortar desde arriba (ej. 0.20 para 20%).
 * @returns {HTMLCanvasElement} - Un nuevo elemento canvas con la imagen recortada.
 */
export const cropHeader = (sourceImage, originalWidth, originalHeight, topCropRatio = 0.20) => {
  if (!sourceImage) {
    throw new Error('sourceImage is required');
  }

  // Calculamos los píxeles exactos a recortar (redondeo hacia abajo para asegurar la eliminación)
  const cropHeightPixels = Math.floor(originalHeight * topCropRatio);
  
  // Calculamos las dimensiones resultantes del cuerpo evaluable
  const resultingHeight = originalHeight - cropHeightPixels;
  const resultingWidth = originalWidth;

  // Creamos el canvas de destino (lógica separada del I/O de red)
  const canvas = document.createElement('canvas');
  canvas.width = resultingWidth;
  canvas.height = resultingHeight;

  const ctx = canvas.getContext('2d');
  
  // Dibujamos la imagen desplazada hacia arriba para recortar la parte superior
  // ctx.drawImage(image, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight)
  ctx.drawImage(
    sourceImage, 
    0, cropHeightPixels, resultingWidth, resultingHeight, 
    0, 0, resultingWidth, resultingHeight 
  );

  return canvas;
};
