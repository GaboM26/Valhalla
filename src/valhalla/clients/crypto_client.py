import os
import sys

# Odin - the allfather that can see it all will determine
# if you are worthy of the passwords or not. Only the allfather,
# with a password only he knows, will be able to check
# (hash passwords) to verify the identity of those with the desire
# to access Valhalla.

class CryptoClient:

    def __init__(self, configs:dict):
        self._odin = configs['odin_password']

    def hash(self, raw_password):
        pass

    def hash_diff(self, raw_password, hashed_password):
        pass

    def encrypt(self, password, txt):
        pass

    def decrypt(self, password, txt):
        pass