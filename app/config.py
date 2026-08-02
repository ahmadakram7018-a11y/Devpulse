from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY : str
    Debug: bool=True
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    TEST_DATABASE_URL : str

    class Config:
        env_file = ".env"


settings = Settings()
