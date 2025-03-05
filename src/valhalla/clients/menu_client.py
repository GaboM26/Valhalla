from time import sleep
from src.valhalla.constants.menu_options import (
    SUPPORTED_OPTIONS,
    NUM_POINTS,
    SUSPENSE_CREATOR_AMOUNT,
    STARLINE,
    VALHALLA_BANNER,
    VALHALLA_CREDITS,
    ODIN_PERMISSIONS
)
from src.valhalla.constants.const import (
    SECRETS_TABLE_NAME
)
import getpass
from src.valhalla.utils.payload_builder import PayloadBuilder

class MenuClient:

    def __init__(self, credentials, sql_client, crypto_tools):
        self._username, self._password = credentials
        self._sql_client = sql_client
        self._crypto_tools = crypto_tools
        self._payload_builder = PayloadBuilder()

    def run(self):
        self.welcome_message()
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == 'q':
                break
            self.execute_option(choice)

    def display_menu(self):
        print(STARLINE)
        for key, value in SUPPORTED_OPTIONS.items():
            print(f"{key}: {value[1]}")

    def execute_option(self, choice):
        try:
            option = SUPPORTED_OPTIONS[int(choice)][0]
            method = getattr(self, option)
            method()
        except (KeyError, AttributeError, ValueError) as e:
            print(f"Invalid option: {e}")

    def new_entry(self):
        app_name = input("Enter the app name (i.e Facebook): ")

        # TODO: add check for already existing app name, ask if update or not

        username = input("Enter the username (i.e gabo_m26): ")
        password = getpass.getpass("Enter the password: ")
        app_name_enc = self._crypto_tools.encrypt(self._password, app_name)
        username_enc = self._crypto_tools.encrypt(self._password, username)
        password_enc = self._crypto_tools.encrypt(self._password, password)
        
        self._sql_client.insert_row_table(SECRETS_TABLE_NAME, 
                                          self._payload_builder.build(SECRETS_TABLE_NAME)(app_name_enc, 
                                                                                          username_enc, 
                                                                                          password_enc,
                                                                                          self._username))
        print("New entry added successfully")

    def view_accounts(self):
        print("Executing view_accounts method")
    
    def get_entry(self):
        print("Executing get_entry method")
    
    def welcome_message(self):
        msg = f'Welcome {self._username} to'
        print(msg, end='', flush=True)
        for i in range(NUM_POINTS):
            print('.', end='', flush=True)
            sleep(SUSPENSE_CREATOR_AMOUNT)
        print('')
        print(STARLINE)
        print(VALHALLA_BANNER)
        print(VALHALLA_CREDITS)

        if self._crypto_tools.is_odin(self._username):
            print(ODIN_PERMISSIONS)