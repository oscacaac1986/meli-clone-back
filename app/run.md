# 🚀 MercadoLibre Clone - Backend FastAPI

## 📋 Prerrequisitos

### Software Requerido
- **Python 3.8+**
- **pip** (incluido con Python)

### Verificar Instalación
```bash
python --version     # Debe mostrar 3.8+
pip --version        # Debe mostrar 20.0+

meli-clone-back/
├── app/
│   ├── main.py              # Aplicación principal
│   ├── routers/             # Endpoints REST
│   ├── services/            # Lógica de negocio async
│   ├── models/              # Modelos Pydantic
│   ├── middleware/          # Error handling
│   └── data/                # Datos mock (JSON)
├── static/
│   └── images/              # Imágenes de productos
├── tests/                   # Tests unitarios
├── requirements.txt         # Dependencias Python
└── run.md                  # Este archivo

git clone https://github.com/oscacaac1986/meli-clone-back.git
cd meli-clone-back

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

# Crear imágenes SVG de productos
python create_simple_images.py

### Inicializar servidor
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

### Ejecutar test

pytest tests/ -v

pytest --cov=app --cov-report=html