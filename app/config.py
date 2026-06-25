from pydantic import BaseSettings

class Settings(BaseSettings):
    Database_URL: str
    SECRET_KEY : str
    Debug: bool=True

    class config:
        env_file = ".env"