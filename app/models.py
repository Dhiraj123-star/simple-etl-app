from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class SalesData(Base):
    __tablename__ = "sales_data"
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    category = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer)
    total_amount = Column(Float)
    sale_date = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())