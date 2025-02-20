import unittest
from unittest.mock import patch, MagicMock
from src.valhalla.clients.crypto_client import CryptoClient
import subprocess

# FILE: src/valhalla/clients/test_crypto_client.py


class TestCryptoClient(unittest.TestCase):

    @patch('src.valhalla.clients.crypto_client.CryptoClient.prepare_tools', return_value=None)
    def setUp(self, MockPrepareTools):
        self.configs = {
            'odin_username':'odin',
            'odin_password': 'secret'
        }
        self.project_root = '/mock/project/root'
        self.client = CryptoClient(self.configs, self.project_root)
        self.raw_password = 'password123'

    @patch('subprocess.run')
    def test_hash(self, mock_subprocess_run):
        mock_subprocess_run.return_value = MagicMock(stdout='hashed_password\n', returncode=0)
        result = self.client.hash(self.raw_password)

        mock_subprocess_run.assert_called_once_with(['./hmac', '-h', '-p', 'secret', self.raw_password],
                                                    cwd=self.client._tools_path,
                                                    capture_output=True,
                                                    text=True, 
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

if __name__ == "__main__":
    unittest.main()