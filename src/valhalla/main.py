import sys
import os
import argparse

# Ensure the project root is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

from src.valhalla.clients.driver_client import DriverClient
from src.valhalla.utils.parser import ValhallaConfigParser
from src.valhalla.constants.const import DEFAULT

def parse_config():
    config_parser = ValhallaConfigParser()

def main():

    config = parse_config()
    driver = DriverClient()

    # Other Logic (secret retrieval, etc...)

    driver.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Valhalla Command Line Interface")
    parser.add_argument('--config', type=str, default=DEFAULT, help='Path to secrets file')
    parser.add_argument('--run-mode', type=str, choices=['default', 'custom'], default='default', help='Mode to run the driver client')
    
    args = parser.parse_args()
    main()