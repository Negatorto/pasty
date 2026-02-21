import json
import os

class ConfigManager:
    def __init__(self):
        config_dir = os.path.expanduser("~/.config/pasty")
        os.makedirs(config_dir, exist_ok=True)
        self.config_file = os.path.join(config_dir, "config.json")
        self.config = {}
        self.load()

    def load(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                self.config = {}
        else:
            self.config = {}

    def save(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save()
