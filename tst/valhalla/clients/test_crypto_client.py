import unittest
from unittest.mock import patch, MagicMock
from src.valhalla.clients.crypto_client import CryptoClient
import subprocess
import os

# FILE: src/valhalla/clients/test_crypto_client.py


class TestCryptoClient(unittest.TestCase):

    @patch('src.valhalla.clients.crypto_client.CryptoClient.prepare_tools', return_value=None)
    def setUp(self, MockPrepareTools):
        self.configs = {
            'odin_username':'odin',
            'odin_password': 'secret'
        }
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
        self.client = CryptoClient(self.configs, self.project_root)
        self.raw_password = 'password123'

    @patch('subprocess.run')
    def test_hash(self, mock_subprocess_run):
        mock_subprocess_run.return_value = MagicMock(stdout='hashed_password\n', returncode=0)
        result = self.client.hash(self.raw_password)

        mock_subprocess_run.assert_called_once_with(['./hmac', '-h', '-p', 'secret', self.raw_password],
                                                    cwd=self.client._tools_path,
                                                    capture_output=True,
                                                    text=False, 
                                                    check=True)
        self.assertEqual(result, 'hashed_password')

    @patch('subprocess.run')
    def test_hash_diff_match(self, mock_subprocess_run):
        mock_subprocess_run.return_value = MagicMock(stdout='Hashes match.\n', returncode=0)
        hashed_password = 'hashed_password'
        result = self.client.hash_diff(self.raw_password, hashed_password)
        
        mock_subprocess_run.assert_called_once_with(['./hmac', '-h', self.raw_password, '-p', 'secret', '-v', hashed_password],
                                                    cwd=self.client._tools_path,
                                                    capture_output=True,
                                                    text=True, 
                                                    check=True)
        self.assertFalse(result)

    @patch('subprocess.run')
    def test_hash_diff_no_match(self, mock_subprocess_run):
        mock_subprocess_run.return_value = MagicMock(stdout='Hashes do not match.\n', returncode=0)
        hashed_password = 'hashed_password'
        result = self.client.hash_diff(self.raw_password, hashed_password)
        
        mock_subprocess_run.assert_called_once_with(['./hmac', '-h', self.raw_password, '-p', 'secret', '-v', hashed_password],
                                                    cwd=self.client._tools_path,
                                                    capture_output=True,
                                                    text=True, 
                                                    check=True)
        self.assertTrue(result)

    @patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'bin/hmac'))
    def test_hash_diff_error(self, mock_subprocess_run):
        hashed_password = 'hashed_password'
        result = self.client.hash_diff(self.raw_password, hashed_password)
        
        mock_subprocess_run.assert_called_once_with(['./hmac', '-h', self.raw_password, '-p', 'secret', '-v', hashed_password],
                                                    cwd=self.client._tools_path,
                                                    capture_output=True,
                                                    text=True, 
                                                    check=True)
        self.assertTrue(result)

    
    def test_encrypt_returns_str(self):
        plaintext = 'test'
        ciphertext = self.client.encrypt('password', plaintext)
        self.assertIsInstance(ciphertext, str)
        try:
            int(ciphertext)
        except ValueError:
            self.fail("ciphertext is not converted to int properly")
    
    def test_decrypt_returns_str(self):
        plaintext = 'test'
        ciphertext = self.client.encrypt('password', plaintext)
        decrypted = self.client.decrypt('password', ciphertext)
        self.assertIsInstance(decrypted, str)
        self.assertEqual(plaintext, decrypted)


if __name__ == "__main__":
    unittest.main()