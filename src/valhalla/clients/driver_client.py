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
from src.valhalla.clients.menu_client import MenuClient

class DriverClient:

    def __init__(self, secrets, project_root):
        self._sqlClient = PyMySqlClient(secrets['database_user'], secrets['database_password'],
                                  secrets['host'], secrets['database'])
        self._crypto_tools = CryptoClient(secrets['crypto_specs'], project_root)

    def run(self):
        if(not self._sqlClient.database_exists()):
            raise ValueError(f"Database '{self._sqlClient.get_db()}' does not exist.")
        
        auth_user_credentials = self.get_authorized_creds()
        
        if(auth_user_credentials is None):
            # TODO: Should keep these in a table to keep a log of unauthorized access attempts
            raise UnauthorizedUserError
        
        # We know user is authenticated
        # TODO: potentially, when use cases grow we could use some kind of injector here that chooses different
        # super class "helper_client" instances
        menu = MenuClient(auth_user_credentials, self._sqlClient, self._crypto_tools)
        menu.run()
    
    def get_authorized_creds(self):

        for _ in range(MAX_RETRIES_ALLOWED):
            try: 
                username, password = self.validate_input()
                return (username, password)
            except UnauthorizedUserError as e:
                print(f"Username/Password Incorrect - {e}")
        return None
    
    def validate_input(self):
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
