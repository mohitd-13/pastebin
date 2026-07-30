from pathlib import Path
from functools import lru_cache, cached_property

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    POSTGRES_DRIVER: str = "asyncpg"
    POSTGRES_USER: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "example"
    POSTGRES_PASSWORD_FILE: str = "./secrets/postgresql/credential"

    @cached_property
    def postgres_password(self) -> str:
        path = Path(self.POSTGRES_PASSWORD_FILE)
        if not path.is_file():
            raise ValueError(f"Password file not found {path}")
        password = path.read_text(encoding="utf-8").strip()
        if not password:
            raise ValueError("Password not found, file is empty")
        return password
    
    @cached_property
    def postgres_url(self) -> str:
        return (
            f"postgresql+{self.POSTGRES_DRIVER}://"
            f"{self.POSTGRES_USER}:{self.postgres_password}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        
@lru_cache
def get_settings() -> Settings:
    """
    This function ensures that the settings are loaded only once
    and cached for future use.
    """
    return Settings()
    
settings = get_settings()