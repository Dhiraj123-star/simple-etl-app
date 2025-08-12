import pandas as pd
import os
from sqlalchemy.orm import Session
from .models import SalesData
from .database import engine, Base
from typing import Dict, Any

def create_tables():
    """Create database tables"""
    Base.metadata.create_all(bind=engine)

def extract_data(file_path: str) -> pd.DataFrame:
    """Extract data from CSV file"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")
    
    df = pd.read_csv(file_path)
    print(f"Extracted {len(df)} records from {file_path}")
    return df

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform the data"""
    # Basic transformations
    df = df.copy()
    
    # Clean column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Handle missing values
    df = df.dropna()
    
    # Calculate total amount if not present
    if 'total_amount' not in df.columns and 'price' in df.columns and 'quantity' in df.columns:
        df['total_amount'] = df['price'] * df['quantity']
    
    # Convert data types
    numeric_columns = ['price', 'quantity', 'total_amount']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remove any rows with NaN values after conversion
    df = df.dropna()
    
    print(f"Transformed data: {len(df)} records remaining")
    return df

def load_data(df: pd.DataFrame, db: Session) -> int:
    """Load data into PostgreSQL"""
    records_inserted = 0
    
    for _, row in df.iterrows():
        sales_record = SalesData(
            product_name=row.get('product_name', ''),
            category=row.get('category', ''),
            price=float(row.get('price', 0)),
            quantity=int(row.get('quantity', 0)),
            total_amount=float(row.get('total_amount', 0)),
            sale_date=str(row.get('sale_date', ''))
        )
        
        db.add(sales_record)
        records_inserted += 1
    
    db.commit()
    print(f"Loaded {records_inserted} records into database")
    return records_inserted

def run_etl_process(file_path: str, db: Session) -> Dict[str, Any]:
    """Run the complete ETL process"""
    try:
        # Create tables if they don't exist
        create_tables()
        
        # Extract
        df = extract_data(file_path)
        
        # Transform
        df_transformed = transform_data(df)
        
        # Load
        records_processed = load_data(df_transformed, db)
        
        return {
            "status": "success",
            "message": "ETL process completed successfully",
            "records_processed": records_processed
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"ETL process failed: {str(e)}",
            "records_processed": 0
        }