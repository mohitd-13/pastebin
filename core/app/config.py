from pathlib import Path
from functools import lru_cache, cached_property

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Connection pool settings
    db_pool_size: int = 5               # Number of permanent connection to keep open in pool
    db_max_overflow: int = 10           # Extra connections allowed during peak load
    db_pool_timeout: int = 30           # Seconds to wait for available connection
    db_pool_recycle: int = 1800         # Recycle connections after 30 minutes
    db_echo: bool = True                # Print SQL in terminal, good for debugging (disable in production)
    
    # Database settings
    postgres_driver: str = "asyncpg"
    postgres_user: str = "postgres"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "example"
    postgres_password_file: str = "./secrets/postgresql/credential"

    @cached_property
    def postgres_password(self) -> str:
        path = Path(self.postgres_password_file)
        if not path.is_file():
            raise ValueError(f"Password file not found {path}")
        password = path.read_text(encoding="utf-8").strip()
        if not password:
            raise ValueError("Password not found, file is empty")
        return password
    
    @cached_property
    def postgres_url(self) -> str:
        return (
            f"postgresql+{self.postgres_driver}://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
        
@lru_cache
def get_settings() -> Settings:
    """
    This function ensures that the settings are loaded only once
    and cached for future use.
    """
    return Settings()
    
settings = get_settings()