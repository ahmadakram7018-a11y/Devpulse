from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    Database_URL: str
    SECRET_KEY : str
    Debug: bool=True

    class Config:
        env_file = ".env"


settings = Settings()
