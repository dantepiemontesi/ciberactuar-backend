"""
CiberActuar — Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "CiberActuar API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Security
    SECRET_KEY: str = "change-this-in-production-please"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 3600  # 1 hour

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://ciberactuar.com",
        "https://www.ciberactuar.com",
    ]

    # Actuarial Model Parameters
    DEFAULT_COVERAGE_AMOUNT: float = 100_000.0
    MONTE_CARLO_SIMULATIONS: int = 10_000
    POISSON_LAMBDA_BASE: float = 0.3  # Average attacks per year for SME

    # Premium Calculation
    LOSS_RATIO: float = 0.60  # Industry standard: 60% of premium covers claims
    EXPENSE_RATIO: float = 0.25  # 25% operational expenses
    PROFIT_MARGIN: float = 0.15  # 15% profit margin

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
