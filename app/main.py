import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.middleware.error_handler import ErrorHandler, logging_middleware
from app.routers import products

# Cargar variables de entorno
load_dotenv()

# Crear aplicación FastAPI con documentación mejorada
app = FastAPI(
    title="MercadoLibre API",
    description="""
    ## API REST para sistema de productos estilo MercadoLibre
    
    Esta API proporciona endpoints para:
    * **Productos**: CRUD completo para productos
    * **Imágenes**: Servicio de imágenes estáticas
    * **Búsqueda**: Búsqueda y filtrado de productos
    * **Categorías**: Gestión de categorías
    
    ### Características
    - Manejo robusto de errores
    - Logging detallado
    - Validación de datos
    - Documentación automática
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "MercadoLibre Clone API",
        "email": "admin@mercadolibre-clone.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Configurar CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Agregar middleware de logging
app.middleware("http")(logging_middleware)

# Configurar manejadores de errores
app.add_exception_handler(RequestValidationError, ErrorHandler.validation_exception_handler)
app.add_exception_handler(Exception, ErrorHandler.general_exception_handler)

# Montar archivos estáticos
static_dir = Path("static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir routers
app.include_router(products.router)

@app.get("/", tags=["Health"])
async def root():
    """
    Endpoint raíz con información de la API
    
    Returns:
        dict: Información básica de la API
    """
    return {
        "message": "MercadoLibre API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "active",
        "features": [
            "Error handling",
            "Request logging", 
            "Data validation",
            "Static file serving"
        ]
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Endpoint de verificación de salud del servicio
    
    Returns:
        dict: Estado de salud del servicio
    """
    try:
        images_dir = Path("static/images/products")
        images_count = len(list(images_dir.glob("*.svg"))) if images_dir.exists() else 0
        
        return {
            "status": "healthy",
            "message": "API funcionando correctamente",
            "checks": {
                "static_directory": static_dir.exists(),
                "images_available": images_count,
                "database": "mock_data_ok"
            },
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Error en health check: {str(e)}",
            "version": "1.0.0"
        }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true",
        log_level="info"
    )