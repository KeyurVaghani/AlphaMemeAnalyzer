from typing import List, Optional, Union, Dict, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, field_validator
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Memecoin Alpha Hunter System"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "mahs")
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode='before')
    def assemble_db_connection(cls, v: Optional[str], info: Dict[str, Any]) -> str:
        if v:
            return v
        
        # Get values from the model's data
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "password")
        server = os.getenv("POSTGRES_SERVER", "localhost")
        db = os.getenv("POSTGRES_DB", "mahs")
        
        return f"postgresql://{user}:{password}@{server}/{db}"

    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API Keys
    INFURA_API_KEY: str = os.getenv("INFURA_API_KEY", "")
    TWITTER_API_KEY: str = os.getenv("TWITTER_API_KEY", "")
    TWITTER_API_SECRET: str = os.getenv("TWITTER_API_SECRET", "")
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    ETHERSCAN_API_KEY: str = os.getenv("ETHERSCAN_API_KEY", "")
    BSCSCAN_API_KEY: str = os.getenv("BSCSCAN_API_KEY", "")
    
    # Email Configuration
    EMAIL_SENDER: str = os.getenv("EMAIL_SENDER", "")
    EMAIL_RECIPIENT: str = os.getenv("EMAIL_RECIPIENT", "")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")
    
    # Discord Configuration
    DISCORD_WEBHOOK_URL: str = os.getenv("DISCORD_WEBHOOK_URL", "")
    
    # Social Media Settings
    TWITTER_FETCH_INTERVAL: int = 300  # 5 minutes
    TELEGRAM_FETCH_INTERVAL: int = 300
    REDDIT_FETCH_INTERVAL: int = 300
    
    # Blockchain Settings
    BLOCKCHAIN_SCAN_INTERVAL: int = 60  # 1 minute
    MIN_LIQUIDITY_USD: float = float(os.getenv("MIN_LIQUIDITY_USD", "50000"))
    MIN_HOLDERS: int = int(os.getenv("MIN_HOLDERS", "100"))
    
    # Analysis Settings
    SENTIMENT_THRESHOLD: float = float(os.getenv("SENTIMENT_THRESHOLD", "0.7"))
    VOLUME_SPIKE_THRESHOLD: float = float(os.getenv("VOLUME_SPIKE_THRESHOLD", "2.0"))
    SOCIAL_ENGAGEMENT_THRESHOLD: int = int(os.getenv("SOCIAL_ENGAGEMENT_THRESHOLD", "1000"))
    
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings() 