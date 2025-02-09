from src.valhalla.clients.mysql_client import PyMySqlClient
from src.valhalla.utils.exceptions.unauthorized_user_error import UnauthorizedUserError
import getpass
from src.valhalla.constants.const import (
    MAX_RETRIES_ALLOWED,
    MASTER_TABLE_NAME,
    HASHED_MASTER_PASSWORD_FIELD_NAME,
    MASTER_FIELD_NAME
)
from src.valhalla.clients.crypto_client import CryptoClient
import sys

class DriverClient:

    def __init__(self, secrets):
        self._sqlClient = PyMySqlClient(secrets['database_user'], secrets['database_password'],
                                  secrets['host'], secrets['database'])
        self._crypto_tools = CryptoClient(secrets['crypto_specs'])
        self._username = None
        self._password = None

    def run(self):
        if(not self._sqlClient.database_exists()):
            raise ValueError(f"Database '{self._sqlClient.get_db()}' does not exist.")
        
        retry_count = 0
        
        while retry_count < MAX_RETRIES_ALLOWED:
            try: 
                self._username, self._password = self.validate_authorized_user()
                break
            except UnauthorizedUserError as e:
                print(f"Username/Password Incorrect - {e}")
                retry_count += 1
        
        if (self._username == None and self._password == None):
            print("Too many retries. Attempts logged. Contact DB Administrator to unblock")
            # TODO: Should keep these in a table to keep a log of unauthorized access attempts
            sys.exit()
        
        print(self.welcome_message())

        self.display_menu()
    
    def welcome_message(self):
        msg = f'Welcome {self._username}'
        if(self._crypto_tools.is_odin(self._username)):
            return msg + ', Odin permissions granted'
        #TODO: admin benefits could be awarded 
        return msg + ', Einherjar. What can Valhalla give you today?'
    
    def validate_authorized_user(self):
        usr, ps = self.get_user_credentials()
        get_list = [HASHED_MASTER_PASSWORD_FIELD_NAME]
        filter_map = {
            MASTER_FIELD_NAME: usr
        }
        ret = self._sqlClient.retrieve(MASTER_TABLE_NAME, get_list, filter_map)

        if(len(ret) != 1 or self._crypto_tools.hash_diff(ps, ret[0]['password'])):
            raise UnauthorizedUserError("Unauthorized User. Blocking")
        

        return usr, ps


    def get_user_credentials(self):
        """
        Prompt the user to input their username and password.
        :return: A tuple containing the username and password.
        """
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")
        return username, password

    def display_menu(self):
        pass