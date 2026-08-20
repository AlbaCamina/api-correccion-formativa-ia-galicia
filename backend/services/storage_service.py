import os
import uuid
import shutil
import logging
from fastapi import UploadFile

logger = logging.getLogger("backend.services.storage_service")

class StorageService:
    def __init__(self):
        self.provider = os.getenv("STORAGE_PROVIDER", "local").lower()
        self.local_upload_dir = "uploads"
        
        if self.provider == "local":
            os.makedirs(self.local_upload_dir, exist_ok=True)
            logger.info("StorageService configurado en modo LOCAL.")
        elif self.provider == "cloudinary":
            logger.info("StorageService configurado en modo CLOUDINARY.")
            # Aquí se inicializaría el SDK de Cloudinary en el futuro
        else:
            logger.warning(f"Proveedor '{self.provider}' no soportado, cayendo a LOCAL.")
            self.provider = "local"
            os.makedirs(self.local_upload_dir, exist_ok=True)

    async def upload_file(self, file: UploadFile, extension: str) -> str:
        """
        Sube el archivo al proveedor configurado y devuelve la URL pública o local.
        """
        filename = f"{uuid.uuid4()}{extension}"
        
        if self.provider == "local":
            return await self._upload_local(file, filename)
        elif self.provider == "cloudinary":
            # YAGNI: Implementación futura. Por ahora, forzamos local.
            # return await self._upload_cloudinary(file, filename)
            logger.warning("Cloudinary no implementado aún, usando almacenamiento local.")
            return await self._upload_local(file, filename)
            
    async def _upload_local(self, file: UploadFile, filename: str) -> str:
        file_path = os.path.join(self.local_upload_dir, filename)
        try:
            with open(file_path, "wb") as buffer:
                while chunk := await file.read(1024 * 1024):
                    buffer.write(chunk)
            return f"/{self.local_upload_dir}/{filename}"
        except Exception as e:
            logger.error(f"Error guardando archivo localmente: {e}")
            raise RuntimeError("Fallo al escribir el archivo en disco local.")
            
storage_service = StorageService()
