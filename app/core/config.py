from functools import lru_cache
from pathlib import Path

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    from pydantic import BaseSettings

    SettingsConfigDict = None

class Settings(BaseSettings):
    BASE_DIR : Path = Path(__file__).parent.parent.parent
    CHROMA_DB_PATH : Path = "./chroma_db"

    OLLAMA_BASE_URL : str = "http://localhost:11434"

    CODER_MODEL: str = "qwen2.5-coder:3b"
    PLANNER_MODEL: str = "phi3:mini"

    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    MAX_ITERATIONS: int = 3
    TEMPERATURE_CODER: float = 0.5
    TEMPERATURE_PLANNER: float = 0.2

    if SettingsConfigDict is not None:
        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            case_sensitive=False,
        )

    else:
        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"
            case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
