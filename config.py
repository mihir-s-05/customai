import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# General Configurations
APP_NAME = "AI Framework Tool"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")

# File Handling
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
ALLOWED_EXTENSIONS = {"csv", "json", "xlsx"}
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 10))  # Max file size in MB

# Model Configuration
MODEL_STORAGE_PATH = os.getenv("MODEL_STORAGE_PATH", "models/")
DEFAULT_MODEL_TYPE = os.getenv("DEFAULT_MODEL_TYPE", "linear_regression")

# API Settings
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8000))

# Logging Configurations
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")

# Database (Optional)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

# Cloud Integration (Optional)
USE_CLOUD_STORAGE = os.getenv("USE_CLOUD_STORAGE", "False").lower() == "true"
CLOUD_BUCKET_NAME = os.getenv("CLOUD_BUCKET_NAME", "")
