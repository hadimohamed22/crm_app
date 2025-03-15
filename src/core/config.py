import json
import os
from typing import Any, Dict

class ConfigManager:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config_data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as config_file:
                    return json.load(config_file)
            return {}
        except Exception as e:
            raise ValueError(f"Failed to load config file: {e}")

    def get(self, section: str = None, key: str = None, default: Any = None) -> Any:
        if section and key:
            return self.config_data.get(section, {}).get(key, default)
        elif section:
            return self.config_data.get(section, default)
        return self.config_data

config = ConfigManager()