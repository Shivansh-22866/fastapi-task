from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str = "MONGODB_URI"
    DATABASE_NAME: str = "task_management"
    SECRET_KEY: str = "your-secret-key"  # In production, use secure environment variable
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()