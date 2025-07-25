import asyncio
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Path, Query

from app.models.product import (ProductListResponse, ProductResponse,
                                ProductSummary)
from app.services.product_service import product_service

router = APIRouter(
    prefix="/api/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=ProductListResponse)
async def get_products(
    skip: int = Query(0, ge=0, description="Número de productos a omitir"),
    limit: int = Query(20, ge=1, le=100, description="Número máximo de productos a retornar"),
    category_id: Optional[str] = Query(None, description="Filtrar por categoría"),
    search: Optional[str] = Query(None, description="Búsqueda por texto"),
    min_price: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Precio máximo")
):
    """
    Obtiene una lista paginada de productos con filtros opcionales.
    """
    # Simular latencia de red
    await asyncio.sleep(0.1)
    
    products = await product_service.get_products(
        skip=skip,
        limit=limit,
        category_id=category_id,
        search=search,
        min_price=min_price,
        max_price=max_price
    )
    
    # Calcular total y paginación (simulado)
    total = len(products) + skip  # Simplificado para el mock
    pages = (total + limit - 1) // limit
    
    return ProductListResponse(
        products=products,
        total=total,
        page=(skip // limit) + 1,
        size=len(products),
        pages=pages
    )

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str = Path(..., description="ID único del producto")
):
    """
    Obtiene los detalles completos de un producto específico,
    incluyendo información del vendedor y productos relacionados.
    """
    # Simular latencia de red
    await asyncio.sleep(0.15)
    
    product = await product_service.get_product_by_id(product_id)
    
    if not product:
        raise HTTPException(
            status_code=404, 
            detail=f"Producto con ID '{product_id}' no encontrado"
        )
    
    return product

@router.get("/search/{query}", response_model=List[ProductSummary])
async def search_products(
    query: str = Path(..., description="Término de búsqueda"),
    limit: int = Query(10, ge=1, le=50, description="Número máximo de resultados")
):
    """
    Búsqueda de productos por término de texto.
    """
    await asyncio.sleep(0.08)
    
    if len(query.strip()) < 2:
        raise HTTPException(
            status_code=400, 
            detail="El término de búsqueda debe tener al menos 2 caracteres"
        )
    
    products = await product_service.search_products(query, limit)
    return products

@router.get("/category/{category_id}", response_model=List[ProductSummary])
async def get_products_by_category(
    category_id: str = Path(..., description="ID de la categoría"),
    limit: int = Query(20, ge=1, le=100, description="Número máximo de productos")
):
    """
    Obtiene productos de una categoría específica.
    """
    await asyncio.sleep(0.1)
    
    products = await product_service.get_products_by_category(category_id, limit)
    return products

@router.get("/{product_id}/related", response_model=List[ProductSummary])
async def get_related_products(
    product_id: str = Path(..., description="ID del producto base"),
    limit: int = Query(4, ge=1, le=10, description="Número máximo de productos relacionados")
):
    """
    Obtiene productos relacionados a un producto específico.
    """
    await asyncio.sleep(0.08)
    
    # Primero verificar que el producto existe
    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=404, 
            detail=f"Producto con ID '{product_id}' no encontrado"
        )
    
    
    # Retornar productos relacionados
    return product.related_products[:limit]

# Al final del archivo app/routers/products.py, agregar:

@router.get("/{product_id}/images")
async def get_product_images_detailed(
    product_id: str = Path(..., description="ID único del producto")
):
    """
    Obtiene información detallada de las imágenes de un producto
    """
    await asyncio.sleep(0.1)  # Simular latencia
    
    try:
        product = await product_service.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Producto {product_id} no encontrado")
        
        # Procesar imágenes para incluir metadatos
        images_with_metadata = []
        for i, image_url in enumerate(product.images):
            images_with_metadata.append({
                "id": i,
                "url": image_url,
                "alt": f"{product.title} - Vista {i+1}",
                "is_primary": i == 0,
                "type": "product_image"
            })
        
        return {
            "product_id": product_id,
            "product_title": product.title,
            "images": images_with_metadata,
            "total_images": len(images_with_metadata),
            "primary_image": images_with_metadata[0] if images_with_metadata else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo imágenes: {str(e)}")