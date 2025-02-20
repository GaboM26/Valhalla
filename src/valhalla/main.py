import sys
import os
import argparse
import logging
from pymysql.err import OperationalError

# Ensure the project root is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

from src.valhalla.clients.driver_client import DriverClient
from src.valhalla.utils.parser import ValhallaConfigParser
from src.valhalla.utils.exceptions.unauthorized_user_error import UnauthorizedUserError
from src.valhalla.constants.const import *
from src.valhalla.utils.exceptions.missing_dependencies_error import MissingDependenciesError

def main(argv):
    parser = ValhallaConfigParser(argv.secrets)
    retval = 0

    try:
        driver = DriverClient(parser.get_secrets(), project_root)
        driver.run()
    except OperationalError as e:
        logging.error(f"OperationalError: {e}")
        print(f"Error: Unable to connect to server. Check secrets file: {e}")
    except UnauthorizedUserError as e:
        logging.error(f"UnauthorizedUserError: {e}")
        print("Too many retries. Attempts logged. Contact DB Administrator to unblock")
    except MissingDependenciesError as e:
        logging.error(f"UnauthorizedUserError: {e}")
        print("Too many retries. Attempts logged. Contact DB Administrator to unblock")
    finally:
        retval = -1
    
    if(retval == 0):
        print('Success')
    return retval

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Welcome to Project Valhalla")
    parser.add_argument('--secrets', type=str, default=DEFAULT_SECRET_PATH, help='Path to secrets file')
    
    args = parser.parse_args()
    main(args)