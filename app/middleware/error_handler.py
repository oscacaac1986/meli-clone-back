import logging
import traceback
import uuid
from datetime import datetime

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ErrorHandler:
    """Manejador centralizado de errores"""
    
    @staticmethod
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Manejar excepciones HTTP"""
        error_id = str(uuid.uuid4())
        
        logger.error(f"HTTP Exception [{error_id}]: {exc.status_code} - {exc.detail}")
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "id": error_id,
                    "type": "http_exception",
                    "status_code": exc.status_code,
                    "message": exc.detail,
                    "timestamp": datetime.now().isoformat(),
                    "path": str(request.url.path)
                }
            }
        )
    
    @staticmethod
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Manejar errores de validación"""
        error_id = str(uuid.uuid4())
        
        logger.error(f"Validation Error [{error_id}]: {exc.errors()}")
        
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "id": error_id,
                    "type": "validation_error",
                    "status_code": 422,
                    "message": "Error de validación en los datos enviados",
                    "details": exc.errors(),
                    "timestamp": datetime.now().isoformat(),
                    "path": str(request.url.path)
                }
            }
        )
    
    @staticmethod
    async def general_exception_handler(request: Request, exc: Exception):
        """Manejar excepciones generales"""
        error_id = str(uuid.uuid4())
        
        logger.error(f"Unhandled Exception [{error_id}]: {str(exc)}")
        logger.error(f"Traceback [{error_id}]: {traceback.format_exc()}")
        
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "id": error_id,
                    "type": "internal_server_error",
                    "status_code": 500,
                    "message": "Error interno del servidor. Contacte al administrador.",
                    "timestamp": datetime.now().isoformat(),
                    "path": str(request.url.path)
                }
            }
        )

# Crear middleware de logging de requests
async def logging_middleware(request: Request, call_next):
    """Middleware para logging de requests"""
    start_time = datetime.now()
    request_id = str(uuid.uuid4())
    
    # Log del request
    logger.info(f"Request [{request_id}]: {request.method} {request.url}")
    
    try:
        response = await call_next(request)
        
        # Calcular tiempo de procesamiento
        process_time = (datetime.now() - start_time).total_seconds()
        
        # Log de la respuesta
        logger.info(f"Response [{request_id}]: {response.status_code} - {process_time:.4f}s")
        
        # Agregar headers de tracking
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
        
    except Exception as e:
        logger.error(f"Request Error [{request_id}]: {str(e)}")
        raise