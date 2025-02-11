from src.valhalla.clients.driver_client import DriverClient
from src.valhalla.clients.crypto_client import CryptoClient


class MenuClient:

    def __init__(self, credentials, sql_client, crypto_tools):
        self._username, self._password = credentials
        self._crypto_tools = crypto_tools
        self._sql_client = sql_client

    def run(self):
        pass

    def welcome_message(self):
        msg = f'Welcome {self._username}'
        if(self._crypto_tools.is_odin(self._username)):
            return msg + ', Odin permissions granted'
        #TODO: admin benefits could be awarded 
        return msg + ', Einherjar. What can Valhalla give you today?'
