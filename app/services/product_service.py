import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.models.product import (Product, ProductColor, ProductCreate,
                                ProductInstallments, ProductResponse,
                                ProductSpecification, ProductSummary,
                                ProductUpdate, Seller)


class ProductService:
    def __init__(self, data_path: str = "app/data"):
        self.data_path = Path(data_path)
        self._products_cache = None
        self._sellers_cache = None
        self._categories_cache = None
    
    async def _load_json_file(self, filename: str) -> Dict[str, Any]:
        """Carga asíncrona de archivos JSON"""
        file_path = self.data_path / filename
        
        def read_file():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Simular operación asíncrona
        await asyncio.sleep(0.01)  # Simular delay de I/O
        return read_file()
    
    async def _get_products_data(self) -> List[Dict]:
        """Obtiene datos de productos con cache"""
        if self._products_cache is None:
            data = await self._load_json_file("products.json")
            self._products_cache = data["products"]
        return self._products_cache
    
    async def _get_sellers_data(self) -> List[Dict]:
        """Obtiene datos de vendedores con cache"""
        if self._sellers_cache is None:
            data = await self._load_json_file("sellers.json")
            self._sellers_cache = data["sellers"]
        return self._sellers_cache
    
    async def _get_categories_data(self) -> List[Dict]:
        """Obtiene datos de categorías con cache"""
        if self._categories_cache is None:
            data = await self._load_json_file("categories.json")
            self._categories_cache = data["categories"]
        return self._categories_cache
    
    def _parse_product(self, product_data: Dict) -> Product:
        """Convierte dict a modelo Product"""
        # Convertir colores
        colors = [
            ProductColor(**color) for color in product_data.get("colors", [])
        ]
        
        # Convertir especificaciones
        specifications = [
            ProductSpecification(**spec) for spec in product_data.get("specifications", [])
        ]
        
        # Convertir installments
        installments_data = product_data.get("installments", {})
        installments = ProductInstallments(**installments_data)
        
        return Product(
            id=product_data["id"],
            title=product_data["title"],
            price=product_data["price"],
            original_price=product_data.get("original_price"),
            currency=product_data["currency"],
            condition=product_data["condition"],
            sold_quantity=product_data["sold_quantity"],
            rating=product_data["rating"],
            reviews_count=product_data["reviews_count"],
            free_shipping=product_data["free_shipping"],
            full_warranty=product_data["full_warranty"],
            mercado_pago=product_data["mercado_pago"],
            category_id=product_data["category_id"],
            seller_id=product_data["seller_id"],
            images=product_data["images"],
            colors=colors,
            specifications=specifications,
            stock=product_data["stock"],
            payment_methods=product_data["payment_methods"],
            installments=installments,
            description=product_data["description"],
            features=product_data["features"],
            created_at=datetime.fromisoformat(product_data["created_at"].replace('Z', '+00:00')),
            updated_at=datetime.fromisoformat(product_data["updated_at"].replace('Z', '+00:00'))
        )
    
    async def get_product_by_id(self, product_id: str) -> Optional[ProductResponse]:
        """Obtiene un producto por ID con información completa"""
        products_data = await self._get_products_data()
        sellers_data = await self._get_sellers_data()
        
        # Buscar el producto
        product_data = next((p for p in products_data if p["id"] == product_id), None)
        if not product_data:
            return None
        
        # Convertir a modelo Product
        product = self._parse_product(product_data)
        
        # Buscar información del vendedor
        seller_data = next((s for s in sellers_data if s["id"] == product.seller_id), None)
        seller = Seller(**seller_data) if seller_data else None
        
        # Buscar productos relacionados (misma categoría, excluyendo el actual)
        related_products_data = [
            p for p in products_data 
            if p["category_id"] == product.category_id and p["id"] != product_id
        ][:4]  # Máximo 4 productos relacionados
        
        related_products = [
            ProductSummary(
                id=p["id"],
                title=p["title"],
                price=p["price"],
                currency=p["currency"],
                image=p["images"][0] if p["images"] else "",
                rating=p["rating"],
                reviews_count=p["reviews_count"],
                free_shipping=p["free_shipping"],
                condition=p["condition"]
            ) for p in related_products_data
        ]
        
        return ProductResponse(
            **product.model_dump(),
            seller=seller,
            related_products=related_products
        )
    
    async def get_products(
        self, 
        skip: int = 0, 
        limit: int = 20,
        category_id: Optional[str] = None,
        search: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[ProductSummary]:
        """Obtiene lista de productos con filtros"""
        products_data = await self._get_products_data()
        
        # Aplicar filtros
        filtered_products = products_data
        
        if category_id:
            filtered_products = [p for p in filtered_products if p["category_id"] == category_id]
        
        if search:
            search_lower = search.lower()
            filtered_products = [
                p for p in filtered_products 
                if search_lower in p["title"].lower() or search_lower in p["description"].lower()
            ]
        
        if min_price is not None:
            filtered_products = [p for p in filtered_products if p["price"] >= min_price]
        
        if max_price is not None:
            filtered_products = [p for p in filtered_products if p["price"] <= max_price]
        
        # Paginación
        paginated_products = filtered_products[skip:skip + limit]
        
        # Convertir a ProductSummary
        return [
            ProductSummary(
                id=p["id"],
                title=p["title"],
                price=p["price"],
                currency=p["currency"],
                image=p["images"][0] if p["images"] else "",
                rating=p["rating"],
                reviews_count=p["reviews_count"],
                free_shipping=p["free_shipping"],
                condition=p["condition"]
            ) for p in paginated_products
        ]
    
    async def search_products(self, query: str, limit: int = 10) -> List[ProductSummary]:
        """Búsqueda de productos por texto"""
        return await self.get_products(limit=limit, search=query)
    
    async def get_products_by_category(self, category_id: str, limit: int = 20) -> List[ProductSummary]:
        """Obtiene productos por categoría"""
        return await self.get_products(limit=limit, category_id=category_id)

# Instancia global del servicio
product_service = ProductService()