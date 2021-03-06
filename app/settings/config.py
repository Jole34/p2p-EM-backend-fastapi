from pydantic import BaseSettings, PostgresDsn, validator
from typing import Optional, Dict, Any, List

from pydantic import AnyHttpUrl

class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost"
    ]

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection_sandbox(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
            port=values.get("POSTGRES_DB_PORT")
        )
        
    class Config:
        case_sensitive = True
        env_file = "app/.env"

settings = Settings()