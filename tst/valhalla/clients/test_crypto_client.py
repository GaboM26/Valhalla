import unittest
from unittest.mock import patch, MagicMock
from src.valhalla.clients.crypto_client import CryptoClient
import subprocess

# FILE: src/valhalla/clients/test_crypto_client.py


class TestCryptoClient(unittest.TestCase):

    def setUp(self):
        self.configs = {'odin_password': 'secret'}
        self.client = CryptoClient(self.configs)

    @patch('subprocess.run')
    def test_hash(self, mock_subprocess_run):
        mock_subprocess_run.return_value = MagicMock(stdout='hashed_password\n', returncode=0)
        raw_password = 'password123'
        result = self.client.hash(raw_password)
        
        mock_subprocess_run.assert_called_once_with(['bin/hmac', '-h', '-p', 'secret', raw_password], capture_output=True, text=True, check=True)
        self.assertEqual(result, 'hashed_password')

    @patch('subprocess.run')
    def test_hash_diff_match(self, mock_subprocess_run):
        mock_subprocess_run.return_value = MagicMock(stdout='Hashes match.\n', returncode=0)
        raw_password = 'password123'
        hashed_password = 'hashed_password'
        result = self.client.hash_diff(raw_password, hashed_password)
        
        mock_subprocess_run.assert_called_once_with(['bin/hmac', '-h', raw_password, '-p', 'secret', '-v', hashed_password], capture_output=True, text=True, check=True)
        self.assertFalse(result)

    @patch('subprocess.run')
    def test_hash_diff_no_match(self, mock_subprocess_run):
        mock_subprocess_run.return_value = MagicMock(stdout='Hashes do not match.\n', returncode=0)
        raw_password = 'password123'
        hashed_password = 'hashed_password'
        result = self.client.hash_diff(raw_password, hashed_password)
        
        mock_subprocess_run.assert_called_once_with(['bin/hmac', '-h', raw_password, '-p', 'secret', '-v', hashed_password], capture_output=True, text=True, check=True)
        self.assertTrue(result)

    @patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'bin/hmac'))
    def test_hash_diff_error(self, mock_subprocess_run):
        raw_password = 'password123'
        hashed_password = 'hashed_password'
        result = self.client.hash_diff(raw_password, hashed_password)
        
        mock_subprocess_run.assert_called_once_with(['bin/hmac', '-h', raw_password, '-p', 'secret', '-v', hashed_password], capture_output=True, text=True, check=True)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()