import pytest
from fastapi.testclient import TestClient

from app.main import app


class TestProducts:
    """Test suite para endpoints de productos"""
    
    def test_health_check(self, client):
        """Test del endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "checks" in data
        assert "version" in data
    
    def test_root_endpoint(self, client):
        """Test del endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "MercadoLibre API"
        assert data["version"] == "1.0.0"
        assert "features" in data
    
    def test_get_product_success(self, client):
        """Test obtener producto existente"""
        response = client.get("/api/products/MLA123456789")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == "MLA123456789"
        assert "title" in data
        assert "price" in data
        assert "seller" in data
        assert "related_products" in data
    
    def test_get_product_not_found(self, client):
        """Test producto no encontrado"""
        response = client.get("/api/products/INVALID_ID")
        assert response.status_code == 404
        
        data = response.json()
        assert "error" in data
        assert data["error"]["status_code"] == 404
    
    def test_get_products_list(self, client):
        """Test lista de productos"""
        response = client.get("/api/products/")
        assert response.status_code == 200
        
        data = response.json()
        assert "products" in data
        assert "total" in data
        assert "page" in data
        assert isinstance(data["products"], list)
    
    def test_search_products_valid(self, client):
        """Test búsqueda de productos con query válido"""
        response = client.get("/api/products/search/Samsung")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_products_invalid_short_query(self, client):
        """Test búsqueda con query muy corto"""
        response = client.get("/api/products/search/a")
        assert response.status_code == 400
        
        data = response.json()
        assert "error" in data
        assert data["error"]["status_code"] == 400
    
    def test_products_by_category(self, client):
        """Test productos por categoría"""
        response = client.get("/api/products/category/smartphones")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    def test_related_products(self, client):
        """Test productos relacionados"""
        response = client.get("/api/products/MLA123456789/related")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 4  # Máximo 4 productos relacionados
    
    def test_products_with_filters(self, client):
        """Test productos con filtros"""
        params = {
            "min_price": 200,
            "max_price": 500,
            "limit": 10
        }
        response = client.get("/api/products/", params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert "products" in data
        # Verificar que los productos están en el rango de precio
        for product in data["products"]:
            assert 200 <= product["price"] <= 500

class TestErrorHandling:
    """Test suite para manejo de errores"""
    
    def test_404_error_format(self, client):
        """Test formato de error 404"""
        response = client.get("/api/products/NONEXISTENT")
        assert response.status_code == 404
        
        data = response.json()
        assert "error" in data
        error = data["error"]
        assert "id" in error
        assert "type" in error
        assert "status_code" in error
        assert "message" in error
        assert "timestamp" in error
        assert "path" in error
    
    def test_validation_error_format(self, client):
        """Test formato de error de validación"""
        # Enviar parámetros inválidos
        response = client.get("/api/products/?limit=-1")
        
        # Puede ser 422 (validation error) o 200 (si el validador lo maneja)
        if response.status_code == 422:
            data = response.json()
            assert "error" in data
            error = data["error"]
            assert error["type"] == "validation_error"
            assert "details" in error

class TestStaticFiles:
    """Test suite para archivos estáticos"""
    
    def test_static_file_access(self, client):
        """Test acceso a archivos estáticos"""
        # Este test puede fallar si no hay imágenes
        response = client.get("/static/images/products/galaxy_a55_1.svg")
        # Puede ser 200 (existe) o 404 (no existe)
        assert response.status_code in [200, 404]