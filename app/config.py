import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Database settings
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "etl_db")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "etl_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "etl_password")
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}")
    LOCAL_DATABASE_URL: str = os.getenv("LOCAL_DATABASE_URL", f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}")
    
    # Application settings
    APP_NAME: str = os.getenv("APP_NAME", "Simple ETL Application")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    
    # Data directory
    DATA_DIR: str = os.getenv("DATA_DIR", "/app/data")

# Create settings instance
settings = Settings()