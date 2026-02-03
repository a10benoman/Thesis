from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    sku: str
    name: str
    category: Optional[str] = None
    unit_cost: Optional[float] = None
    selling_price: Optional[float] = None
    min_stock: Optional[int] = 0
    reorder_point: Optional[int] = 0
    lead_time_days: Optional[int] = 0


class ProductOut(ProductCreate):
    id: int

    class Config:
        orm_mode = True
