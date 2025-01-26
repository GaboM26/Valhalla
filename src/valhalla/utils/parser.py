import sys
import yaml
import os


class ValhallaConfigParser:

    def __init__(self, secrets):
        self.secrets_rel_path = secrets
    
    def get_secrets(self) -> dict:
        secrets_abs_path = os.path.abspath(self.secrets_rel_path)
        if not os.path.exists(secrets_abs_path):
            raise FileNotFoundError(f"Secrets file not found: {secrets_abs_path}")
        with open(secrets_abs_path, 'r') as file:
            config = yaml.safe_load(file)
        return config