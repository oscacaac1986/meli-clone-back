# MercadoLibre Clone - Backend API

## 📖 Descripción
API REST desarrollada con FastAPI que simula las funcionalidades básicas de MercadoLibre, incluyendo gestión de productos, imágenes y búsqueda.

## 🏗️ Arquitectura

app/
├── main.py              # Aplicación principal
├── middleware/          # Middleware personalizado
├── models/             # Modelos Pydantic
├── routers/            # Endpoints organizados
├── services/           # Lógica de negocio
└── data/               # Datos mock (JSON)

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- pip

### Instalación
```bash
# Clonar repositorio
git clone https://github.com/oscacaac1986/meli-clone-back.git
cd meli-clone-back

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Crear datos iniciales
python create_simple_images.py


# Ejecutar servidor
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# 📚 API Endpoints
## Productos

GET /api/products/ - Lista productos con filtros
GET /api/products/{id} - Detalle de producto
GET /api/products/search/{query} - Búsqueda
GET /api/products/category/{category} - Por categoría
GET /api/products/{id}/related - Productos relacionados

Salud y Debug

GET /health - Estado del servicio
GET /debug/files - Debug de archivos estáticos

Archivos Estáticos

/static/images/products/ - Imágenes de productos


# Tests básicos
pytest

# Con coverage
pytest --cov=app --cov-report=html

# Solo tests específicos
pytest tests/test_products.py -v