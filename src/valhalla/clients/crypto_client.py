import os
import sys
import subprocess

# Odin - the allfather that can see it all will determine
# if you are worthy of the passwords or not. Only the allfather,
# with a password only he knows, will be able to check
# (hash passwords) to verify the identity of those with the desire
# to access Valhalla.

class CryptoClient:

    def __init__(self, configs:dict):
        self._odin = configs['odin_password']

    def hash(self, raw_password):
        try:
            result = subprocess.run(['bin/hmac', '-h', '-p', self._odin, raw_password], capture_output=True, text=True, check=True)
            print(result)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error executing hmac: {e}", file=sys.stderr)
            return None

    def hash_diff(self, raw_password, hashed_password):
        try:
            result = subprocess.run(['bin/hmac', '-h', raw_password, '-p', self._odin, '-v', hashed_password], capture_output=True, text=True, check=True)
            stripped_result = result.stdout.strip()
            if(stripped_result== 'Hashes match.'):
                return False
            return True
        except subprocess.CalledProcessError as e:
            # Hash function returned an error (hashes did not match)
            return True
    
    #TODO: Will add additional config in secrets defining true Odin user (db admin)
    def is_odin(self):
        return True

    def encrypt(self, password, txt):
        pass

    def decrypt(self, password, txt):
        pass