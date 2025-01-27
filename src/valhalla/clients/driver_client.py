from src.valhalla.clients.mysql_client import PyMySqlClient
from src.valhalla.utils.exceptions.unauthorized_user_error import UnauthorizedUserError

class DriverClient:

    def __init__(self, secrets):
        self.sqlClient = PyMySqlClient(secrets['database_user'], secrets['database_password'],
                                  secrets['host'], secrets['database'])

    def run(self):
        if(not self.sqlClient.database_exists()):
            raise ValueError(f"Database '{self.sqlClient._database}' does not exist.")
        
        try: 
            self.validate_authorized_user()
            self.execute_menu()
        except UnauthorizedUserError as e:
            print(f"Username/Password Incorrect")
    
    def validate_authorized_user(self):
        pass

    def display_menu(self):
        pass