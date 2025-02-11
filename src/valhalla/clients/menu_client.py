from src.valhalla.constants.menu_options import SUPPORTED_OPTIONS

class MenuClient:

    def __init__(self, credentials, sql_client, crypto_tools):
        self._username, self._password = credentials
        self._sql_client = sql_client
        self._crypto_tools = crypto_tools

    def run(self):
        self.welcome_message()
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == 'q':
                break
            self.execute_option(choice)

    def display_menu(self):
        print("Menu:")
        for key, value in SUPPORTED_OPTIONS.items():
            print(f"{key}: {value[1]}")
        print("q: Quit")

    def execute_option(self, choice):
        try:
            option = SUPPORTED_OPTIONS[int(choice)][0]
            method = getattr(self, option)
            method()
        except (KeyError, AttributeError, ValueError) as e:
            print(f"Invalid option: {e}")

    def new_entry(self):
        print("Executing new_entry method")

    def view_entries(self):
        print("Executing view_entries method")

    def welcome_message(self):
        msg = f'Welcome {self._username}'
        if self._crypto_tools.is_odin(self._username):
            return msg + ', Odin permissions granted'
        return msg + ', Einherjar. What can Valhalla give you today?'