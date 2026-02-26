import json
import os
from src.utils.logger import logger

DEFAULT_CONFIG = {
    "api_key": "",
    "hotkey": "f2",
    "audio_device_index": None, # Default input device
    "target_dbfs": -20.0
}

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = DEFAULT_CONFIG.copy()
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Update config with loaded values, keeping defaults for missing keys
                    self.config.update(loaded_config)
                logger.info(f"Config loaded from {self.config_file}")
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
        else:
            logger.info("Config file not found, using defaults.")
            self.save_config()

    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            logger.info(f"Config saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

# Global instance
config_manager = ConfigManager()
