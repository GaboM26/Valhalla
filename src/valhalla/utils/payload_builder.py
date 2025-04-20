from typing import Callable
from src.valhalla.constants import const


class PayloadBuilder:

    def __init__(self):
        pass


    def build(self, table_name) -> Callable:
        # works as a switch
        switch = {
            const.SECRETS_TABLE_NAME: self.build_secret_entry
        }

        retval = switch.get(table_name, None)

        if(retval is None):
            raise NotImplementedError(f"Table not recognized, can't build payload")
        
        return retval
    
    # Assumes encryption has already taken place
    def build_secret_entry(self, app_name:int, username:int, password:int, valhalla_username:str):
        return {
            const.APPNAME_FIELD: app_name,
            const.USERNAME_FIELD: username,
            const.PASSWORD_FIELD: password,
            const.VALHALLA_USERNAME_FIELD: valhalla_username
        }
    
    def get_encrypted_columns(self, table_name):
        switch = {
            const.SECRETS_TABLE_NAME: [const.APPNAME_FIELD, const.USERNAME_FIELD, const.PASSWORD_FIELD]
        }

        retval = switch.get(table_name, None)

        if(retval is None):
            raise NotImplementedError(f"Table {table_name} not recognized, can't build payload")
        
        return retval
    
    def get_app_name_list(self, table_name):
        switch = {
            const.SECRETS_TABLE_NAME: [const.APPNAME_FIELD]
        }

        retval = switch.get(table_name, None)

        if(retval is None):
            raise NotImplementedError(f"Table {table_name} not recognized, can't build payload")
        
        return retval
    
    def get_valhalla_where_user_payload(self, username):

        where_clause = {
            const.VALHALLA_USERNAME_FIELD: username
        }
        return where_clause
    
    def get_valhalla_where_id_payload(self, id):

        where_clause = {
            const.ID: id
        }
        return where_clause
