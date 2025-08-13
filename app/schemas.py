from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SalesDataBase(BaseModel):
    product_name: str
    category: str
    price: float
    quantity: int
    total_amount: float
    sale_date: str

class SalesDataCreate(SalesDataBase):
    pass

class SalesData(SalesDataBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ETLStatus(BaseModel):
    status: str
    message: str
    records_processed: Optional[int] = None