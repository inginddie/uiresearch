"""Application configuration."""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Crossref configuration
    app_user_agent: str = "CrossrefSearch/1.0"
    app_mailto: str
    crossref_timeout: int = 30
    max_retries: int = 3
    
    # Server configuration
    port: int = 8000
    log_level: str = "INFO"
    
    # CORS configuration
    cors_origins: str = "http://localhost:8000"
    
    # Rate limiting
    rate_limit_searches: str = "10/minute"
    rate_limit_exports: str = "5/minute"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()
