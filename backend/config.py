import os
import yaml
from dataclasses import dataclass
from typing import Optional

@dataclass
class Settings:
    host: str = "0.0.0.0"
    port: int = 8901
    title: str = "NAS Monitor Panel"
    refresh_interval: int = 5
    data_dir: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    ws_enabled: bool = True

def load_settings() -> Settings:
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            return Settings(**config)
    return Settings()

settings = load_settings()