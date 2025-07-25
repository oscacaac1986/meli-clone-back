import pytest

from app.services.product_service import ProductService


class TestProductService:
    """Test suite para ProductService"""
    
    @pytest.fixture
    def product_service(self):
        """Fixture para ProductService"""
        return ProductService()
    
    @pytest.mark.asyncio
    async def test_get_product_by_id_exists(self, product_service):
        """Test obtener producto existente"""
        product = await product_service.get_product_by_id("MLA123456789")
        assert product is not None
        assert product.id == "MLA123456789"
        assert product.title is not None
        assert product.price > 0
    
    @pytest.mark.asyncio
    async def test_get_product_by_id_not_exists(self, product_service):
        """Test obtener producto inexistente"""
        product = await product_service.get_product_by_id("INVALID_ID")
        assert product is None
    
    @pytest.mark.asyncio
    async def test_get_products_with_filters(self, product_service):
        """Test obtener productos con filtros"""
        products = await product_service.get_products(
            skip=0,
            limit=5,
            min_price=100,
            max_price=500
        )
        assert isinstance(products, list)
        assert len(products) <= 5
        
        # Verificar filtro de precio
        for product in products:
            assert 100 <= product.price <= 500
    
    @pytest.mark.asyncio
    async def test_search_products(self, product_service):
        """Test búsqueda de productos"""
        products = await product_service.search_products("Samsung", limit=3)
        assert isinstance(products, list)
        assert len(products) <= 3