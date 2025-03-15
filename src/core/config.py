import json
from pathlib import Path
from typing import Any, Dict
import os

class ConfigManager:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.config_data = self._load_config()
        self.load_config()

    def _load_config(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as config_file:
                    return json.load(config_file)
            return {}
        except Exception as e:
            raise ValueError(f"Failed to load config file: {e}")
        
    def load_config(self):
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                self.config = json.load(f)
        else:
            self.config = {"debug": True}
            self.save_config()

    def save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)

    def get(self, section: str = None, key: str = None, default: Any = None) -> Any:
        if section and key:
            return self.config_data.get(section, {}).get(key, default)
        elif section:
            return self.config_data.get(section, default)
        return self.config_data

    def set(self, key: str, value: Any):
        self.config[key] = value
        self.save_config()

config = ConfigManager()