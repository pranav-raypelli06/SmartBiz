import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = os.getenv("APP_NAME", "SmartBiz Analytics")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    APP_ENV: str = os.getenv("APP_ENV", "development")
    
    DB_HOST: str = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT: int = int(os.getenv("DB_PORT", "3307"))
    DB_USER: str = os.getenv("DB_USER", "smartbiz_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "smartbiz_pass")
    DB_NAME: str = os.getenv("DB_NAME", "smartbiz_db")
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "smartbiz-analytics-super-secret-key-development-2026")
    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
        if origin.strip()
    ]

    @property
    def DATABASE_URL(self) -> str:
        # Standard PyMySQL URL
        pwd = f":{self.DB_PASSWORD}" if self.DB_PASSWORD else ""
        return f"mysql+pymysql://{self.DB_USER}{pwd}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"

settings = Settings()
