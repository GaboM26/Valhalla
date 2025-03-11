import os
import sys
import subprocess
import shutil
import pandas
import tempfile

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
from src.valhalla.utils.payload_builder import PayloadBuilder
from src.valhalla.utils.misc import int_str_to_bytes
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
                                    text=False, 
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

    def encrypt(self, password:str, plaintext:str) -> int:
        try:
            encrypt_cmd_path = os.path.join('.', ENCRYPTOR)
            ciphertext = subprocess.run([encrypt_cmd_path, '-i', plaintext, 'stdout', '-p', password], 
                                    cwd=self._tools_path,
                                    capture_output=True, 
                                    text=False, 
                                    check=True
                                )
        except RuntimeError as e:
            print(f"Error executing encrypt: {e}", file=sys.stderr)
            return None
        return str(int.from_bytes(ciphertext.stdout, 'little'))

    def decrypt(self, password:str, ciphertext_raw_num:str) -> str:
        try:
            decrypt_cmd_path = os.path.join('.', DECRYPTOR)
            ciphertext = int_str_to_bytes(ciphertext_raw_num)

            # Write the bytes to a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(ciphertext)
                temp_file_path = temp_file.name

            plaintext = subprocess.run([decrypt_cmd_path, temp_file_path, 'stdout', '-p', password], 
                                    cwd=self._tools_path,
                                    capture_output=True, 
                                    text=True, 
                                    check=True
                                )
        except RuntimeError as e:
            print(f"Error executing decrypt: {e}", file=sys.stderr)
            return None
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        return plaintext.stdout

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
            print(honir_path)
            compile = subprocess.run(['make', 'all'], cwd=honir_path, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error during compilation: {e.stderr}", file=sys.stderr)
            raise FailedExecutionError("make all")

        # Move required tools to the bin folder
        try:
            self.ensure_directory_exists(self._tools_path)
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
    
    def ensure_directory_exists(self, directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Directory created: {directory_path}")
        else:
            print(f"Directory already exists: {directory_path}")
    
    def decrypt_secrets_df(self, df:pandas.DataFrame, table_name:str, password:str):
        pb = PayloadBuilder()
        df[pb.get_encrypted_columns(table_name)] = df[pb.get_encrypted_columns(table_name)].map(lambda x: self.decrypt(password, x))
        return df