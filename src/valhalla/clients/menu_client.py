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
    ID,
    APPNAME_FIELD
)
import traceback
import getpass
from src.valhalla.utils.payload_builder import PayloadBuilder
from src.valhalla.utils.misc import (
    pretty_print_flat_dict,
    clean_nested_dict
)
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
            print("HERE")
            print(f"Invalid option: {e}")
            traceback.print_exc()

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
        account = input("Enter the app name you want to update (--ls to view accounts): ")

        if(account == "--ls"):
            self.view_accounts()
            account = input("Enter the app name you want to update: ")
        
        self.__update_entry_helper(account)
    
    # performs the update entry process
    def __update_entry_helper(self, account: str):
        # Retrieve the encrypted data for the user
        ciphered_sql_data = self._sql_client.retrieve(
            SECRETS_TABLE_NAME,
            query_dict = self._payload_builder.get_valhalla_where_user_payload(self._username)
        )

        if not ciphered_sql_data:
            print("Valhalla has no records for you yet! Try entering some data first.")
            return

        # Decrypt the data
        df = pandas.DataFrame(ciphered_sql_data)
        unencrypted_df = self._crypto_tools.decrypt_df(
            df,
            SECRETS_TABLE_NAME,
            self._password,
            self._payload_builder.get_encrypted_columns(SECRETS_TABLE_NAME)
        )

        # Check if the account exists
        act = unencrypted_df.loc[unencrypted_df[APPNAME_FIELD] == account]

        if act.empty:
            print(f"Valhalla has no knowledge of '{account}'. You can add it using the new_entry option.")
            return
        
        # filter only relevant fields
        # TODO: Maybe not needed, I believe get_encrypted_columns already does this
        change_fields = act[self._payload_builder.get_encrypted_columns(SECRETS_TABLE_NAME)]
        # Build the update payload
        old_values = clean_nested_dict(change_fields.to_dict())
        update_payload = self.__get_update_fields(old_values)

        if not update_payload:
            print("Valhalla can't update data without your input!")
            return
        # Perform the update
        self._sql_client.update_entry(
            SECRETS_TABLE_NAME,
            update_values=update_payload,
            old_values=old_values,
            pk_vals = self._payload_builder.get_valhalla_where_id_payload(act[ID].values[0])
        )

        print(f"Entry for '{account}' updated successfully.")

    def __get_update_fields(self, account: dict):
        print("select the fields you want to update (press Enter when done):")

        while True:
            print("Current details:")
            pretty_print_flat_dict(account)
            field = input("Enter the field name you want to update (q when done): ")
            if field == 'q':
                break
            if field not in account:
                print(f"Field '{field}' not found in the account details.")
                continue
            new_value = input(f"Enter the new value for '{field}': ")
            if not new_value:
                print("Empty values are not allowed.")
                continue
            # Update the account dictionary
            account[field] = new_value
        
        res = {}
        # Encrypt the updated values
        for key in account.keys():
            if key in self._payload_builder.get_encrypted_columns(SECRETS_TABLE_NAME):
                res[key] = self._crypto_tools.encrypt(self._password, account[key])

        return res


    def delete_entry(self):
        account = input("Enter the app you wish to exile to Hel: ")

        ciphered_sql_data = self._sql_client.retrieve(SECRETS_TABLE_NAME,
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
        
        
        # Perform the delete
        self._sql_client.delete_row(
            SECRETS_TABLE_NAME,
            self._payload_builder.get_valhalla_where_id_payload(act[ID].values[0])
        )

        print(f"Entry for '{account}' exiled to Hel succesfully!")
        
    
    
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