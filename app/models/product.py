from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ProductColor(BaseModel):
    name: str
    available: bool

class ProductSpecification(BaseModel):
    label: str
    value: str

class ProductInstallments(BaseModel):
    available: bool
    count: int
    interest: str

class Seller(BaseModel):
    id: str
    name: str
    reputation: str
    sales: str
    location: str
    rating: float
    years_selling: int
    verified: bool

class ProductBase(BaseModel):
    title: str
    price: float
    currency: str = "US$"
    condition: str = "Nuevo"
    category_id: str
    seller_id: str

class ProductCreate(ProductBase):
    images: List[str] = []
    colors: List[ProductColor] = []
    specifications: List[ProductSpecification] = []
    description: str = ""
    features: List[str] = []
    stock: int = 0

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    description: Optional[str] = None

class Product(ProductBase):
    id: str
    original_price: Optional[float] = None
    sold_quantity: str = "0"
    rating: float = 0.0
    reviews_count: int = 0
    free_shipping: bool = False
    full_warranty: bool = False
    mercado_pago: bool = True
    images: List[str] = []
    colors: List[ProductColor] = []
    specifications: List[ProductSpecification] = []
    stock: int = 0
    payment_methods: List[str] = []
    installments: ProductInstallments
    description: str = ""
    features: List[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductResponse(Product):
    seller: Optional[Seller] = None
    related_products: List['ProductSummary'] = []

class ProductSummary(BaseModel):
    id: str
    title: str
    price: float
    currency: str
    image: str
    rating: float
    reviews_count: int
    free_shipping: bool
    condition: str

class ProductListResponse(BaseModel):
    products: List[ProductSummary]
    total: int
    page: int
    size: int
    pages: int

# Para resolver la referencia circular
ProductResponse.model_rebuild()