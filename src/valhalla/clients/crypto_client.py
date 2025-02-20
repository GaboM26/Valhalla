import os
import sys
import subprocess
import shutil

from src.valhalla.constants.const import (
    CRYPTO_TOOLS_PATH,
    HONIR_REL_PATH,
    HASHER,
    ENCRYPTOR,
    DECRYPTOR,
    AVAILABLE_CRYPTO_TOOLS
)
from src.valhalla.utils.exceptions.missing_dependencies_error import (
    FailedExecutionError,
    MissingDependenciesError
)
# Odin - the allfather that can see it all will determine
# if you are worthy of the passwords or not. Only the allfather,
# with a password only he knows, will be able to check
# (hash passwords) to verify the identity of those with the desire
# to access Valhalla.

class CryptoClient:

    def __init__(self, configs:dict, project_root):
        self._odin_user = configs['odin_username']
        self._odin_pass = configs['odin_password']
        self._tools_path = os.path.join(project_root, CRYPTO_TOOLS_PATH)
        self.prepare_tools(project_root)

    def hash(self, raw_password):
        try:
            hash_cmd = os.path.join('.', HASHER)
            result = subprocess.run([hash_cmd, '-h', '-p', self._odin_pass, raw_password],
                                    cwd=self._tools_path,
                                    capture_output=True,
                                    text=True, 
                                    check=True
                                )
            print(result)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error executing hmac: {e}", file=sys.stderr)
            return None

    def hash_diff(self, raw_password, hashed_password):
        try:
            hash_cmd = os.path.join('.', HASHER)
            result = subprocess.run([hash_cmd, '-h', raw_password, '-p', self._odin_pass, '-v', hashed_password], 
                                    cwd=self._tools_path,
                                    capture_output=True, 
                                    text=True, 
                                    check=True
                                )
            stripped_result = result.stdout.strip()
            if(stripped_result== 'Hashes match.'):
                return False
            return True
        except subprocess.CalledProcessError as e:
            # Hash function returned an error (hashes did not match)
            return True
    
    def is_odin(self, username):
        return self._odin_user == username

    def encrypt(self, password, txt):
        pass

    def decrypt(self, password, txt):
        pass

    def prepare_tools(self, project_root):
        honir_path = os.path.join(project_root, HONIR_REL_PATH)
        if(self.tools_exist()):
            #don't recompile if tools exist
            print("crypto tools found")
            # TODO: add config flag to force re-compilation
            return
        
        print('Crypto tools not found. Attempting Rebuild')

        #Run make in Honir submodule
        try:
            #Will clean executables, compile them, and run unit tests for them
            compile = subprocess.run(['make', 'all'], cwd=honir_path, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error during compilation: {e.stderr}", file=sys.stderr)
            raise FailedExecutionError("make all")

        # Move required tools to the bin folder
        try:
            for tool in AVAILABLE_CRYPTO_TOOLS:
                shutil.move(os.path.join(honir_path, tool), os.path.join(self._tools_path, tool))
        except Exception as e:
            print(f"Error moving tools: {e}", file=sys.stderr)
            raise MissingDependenciesError(tool)

    def tools_exist(self):
        for tool in AVAILABLE_CRYPTO_TOOLS:
            if not os.path.exists(os.path.join(self._tools_path, tool)):
                return False
        return True
    