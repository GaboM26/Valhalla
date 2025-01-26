import sys
import yaml
import os


class ValhallaConfigParser:

    def __init__(self, secrets):
        if(not os.path.isabs(secrets)):
            secrets = self.get_abs_path(secrets)

        if not os.path.exists(secrets):
            raise FileNotFoundError(f"Secrets file not found: {secrets}")

        self.secrets_path = secrets
    
    def get_secrets(self) -> dict:
        with open(self.secrets_path, 'r') as file:
            config = yaml.safe_load(file)
        return config

    def get_abs_path(self, rel_path):
        secrets_abs_path = os.path.abspath(rel_path)
        return secrets_abs_path