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
    SECRETS_TABLE_NAME,
    VALHALLA_USERNAME_FIELD,
    APPNAME_FIELD
)
import getpass
from src.valhalla.utils.payload_builder import PayloadBuilder
from tabulate import tabulate
import pandas

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

        payload = self._payload_builder \
                        .build(SECRETS_TABLE_NAME)(
                            app_name_enc, 
                            username_enc, 
                            password_enc,
                            self._username
                        )

        self._sql_client.insert_row_table(SECRETS_TABLE_NAME, payload)
        print("New entry added successfully")

    def view_accounts(self):

        sql_data = self._sql_client.retrieve(SECRETS_TABLE_NAME,
            field_list = self._payload_builder.get_app_name_list(SECRETS_TABLE_NAME),
            query_dict = self._payload_builder.get_valhalla_where_user_payload(self._username)
        )
        # TODO: It may be a good idea to cache it in order to use the get_entry method later
        df = pandas.DataFrame(sql_data)

        unencrypted_df = self._crypto_tools.decrypt_df(
            df,
            SECRETS_TABLE_NAME,
            self._password, 
            self._payload_builder.get_app_name_list(SECRETS_TABLE_NAME)
        ) 
        print(unencrypted_df)

    
    def get_entry(self):
        account = input("Enter the app you need credentials for: ")

        ciphered_sql_data = self._sql_client.retrieve(SECRETS_TABLE_NAME,
                            field_list = self._payload_builder.get_encrypted_columns(SECRETS_TABLE_NAME),
                            query_dict = self._payload_builder.get_valhalla_where_user_payload(self._username)
                        )
        
        if not ciphered_sql_data:
            print("Valhalla has no records for you yet! Try entering some data first.")
            return

        df = pandas.DataFrame(ciphered_sql_data)
        unencrypted_df = self._crypto_tools.decrypt_df(
            df,
            SECRETS_TABLE_NAME,
            self._password, 
            self._payload_builder.get_encrypted_columns(SECRETS_TABLE_NAME)
        )

        act = unencrypted_df.loc[unencrypted_df[APPNAME_FIELD] == account]
        if act.empty:
            print(f"Valhalla has no knowledge of '{account}'.")
            return
        print(act)
    
    def update_entry(self):
        pass

    def delete_entry(self):
        pass
    
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