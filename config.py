from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# TODO: Add validation for environment variables
# TODO: Add configuration for different environments (dev, staging, prod)
# TODO: Add secrets management

# Load environment variables
# Had to switch to python-dotenv after env vars weren't loading properly
load_dotenv()

class Settings(BaseSettings):
    # Application
    # These were hardcoded before - bad practice!
    APP_NAME: str = "MshiyanePay"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False  # Set to True when debugging
    ENVIRONMENT: str = "development"  # Change this in production!
    
    # Security
    # Make sure to change these in production!
    SECRET_KEY: str  # Used for JWT signing
    ALGORITHM: str = "HS256"  # Standard JWT algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Might need to adjust based on user feedback
    
    # Database
    # Started with SQLite, moved to PostgreSQL
    DATABASE_URL: str
    DATABASE_ENCRYPTION_KEY: str  # For encrypting sensitive data
    
    # SSL/TLS
    # Had to learn about SSL certificates the hard way
    SSL_KEYFILE: Optional[str] = None
    SSL_CERTFILE: Optional[str] = None
    
    # Rate Limiting
    # Added after getting DDoS'd during testing
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Logging
    # Added after debugging became impossible
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # CORS
    # Had to learn about CORS after frontend couldn't connect
    CORS_ORIGINS: list = ["*"]  # Restrict this in production!
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
# This is used throughout the app
settings = Settings()

# Validate required settings
# Added this after deployment failed due to missing env vars
def validate_settings():
    required_settings = [
        "SECRET_KEY",
        "DATABASE_URL",
        "DATABASE_ENCRYPTION_KEY"
    ]
    
    missing_settings = [
        setting for setting in required_settings
        if not getattr(settings, setting)
    ]
    
    if missing_settings:
        raise ValueError(
            f"Missing required settings: {', '.join(missing_settings)}"
        )

# Validate settings on import
# This prevents the app from starting with invalid config
validate_settings() 