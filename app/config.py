from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    Database_URL: str
    SECRET_KEY : str
    Debug: bool=True
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
