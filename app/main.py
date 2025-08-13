from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os

from .database import get_db, engine
from .models import Base
from .schemas import SalesData, ETLStatus
from .etl import run_etl_process
from .config import settings
from . import models

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME, 
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

@app.get("/")
def read_root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}

@app.post("/etl/run", response_model=ETLStatus)
def run_etl(file_name: str = "sample_data.csv", db: Session = Depends(get_db)):
    """Run ETL process on the specified file"""
    file_path = os.path.join(settings.DATA_DIR, file_name)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_name} not found")
    
    result = run_etl_process(file_path, db)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    
    return ETLStatus(**result)

@app.get("/sales/", response_model=List[SalesData])
def get_sales_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get sales data from database"""
    sales = db.query(models.SalesData).offset(skip).limit(limit).all()
    return sales

@app.get("/sales/count")
def get_sales_count(db: Session = Depends(get_db)):
    """Get total count of sales records"""
    count = db.query(models.SalesData).count()
    return {"total_records": count}

@app.delete("/sales/clear")
def clear_sales_data(db: Session = Depends(get_db)):
    """Clear all sales data"""
    deleted_count = db.query(models.SalesData).delete()
    db.commit()
    return {"message": f"Deleted {deleted_count} records"}

@app.get("/config")
def get_config():
    """Get application configuration (excluding sensitive data)"""
    return {
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION,
        "debug": settings.DEBUG,
        "database_name": settings.POSTGRES_DB,
        "database_user": settings.POSTGRES_USER,
        "data_directory": settings.DATA_DIR
        # Note: Password is not exposed for security
    }