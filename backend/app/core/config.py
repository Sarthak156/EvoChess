from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    app_name: str='Adaptive Chess RL'; database_url: str='sqlite:///./adaptive_chess.db'; cors_origins: list[str]=['http://localhost:5173']
    model_path: str='saved_models/ppo_rule_selector.zip'; log_level: str='INFO'
    class Config: env_file='.env'
settings=Settings()
