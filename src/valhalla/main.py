import sys
import os
import argparse

# Ensure the project root is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

from src.valhalla.clients.driver_client import DriverClient
from src.valhalla.utils.parser import ValhallaConfigParser
from src.valhalla.constants.const import *

def main(argv):
    parser = ValhallaConfigParser(argv.secrets)
    driver = DriverClient(parser.get_secrets())

    driver.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Welcome to Project Valhalla")
    parser.add_argument('--secrets', type=str, default=DEFAULT_SECRET_PATH, help='Path to secrets file')
    
    args = parser.parse_args()
    main(args)