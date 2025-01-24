import sys
import os
import argparse

# Ensure the project root is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

from src.valhalla.clients.driver_client import DriverClient
from src.valhalla.utils.parser import ValhallaConfigParser
from src.valhalla.constants.const import *

def parse_config():
    config_parser = ValhallaConfigParser()

def main(argv):
    config = parse_config()
    driver = DriverClient()

    # Other Logic (secret retrieval, etc...)

    driver.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Welcome to Project Valhalla")
    parser.add_argument('--config', type=str, default=DEFAULT, help='Path to secrets file')
    parser.add_argument('--run-mode', type=str, choices=['enc', 'dec', 'ls'], default=DECRYPT, help='Mode \
                        to run the driver client')
    
    args = parser.parse_args()
    main(args)