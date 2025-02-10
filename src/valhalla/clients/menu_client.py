


class MenuClient:

    def __init__(self, credentials):
        self._username, self._password = credentials

    def run(self):
        pass

    def welcome_message(self):
        msg = f'Welcome {self._username}'
        if(self._crypto_tools.is_odin(self._username)):
            return msg + ', Odin permissions granted'
        #TODO: admin benefits could be awarded 
        return msg + ', Einherjar. What can Valhalla give you today?'
