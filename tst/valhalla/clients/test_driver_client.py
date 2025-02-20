import unittest
from unittest.mock import patch, MagicMock
from src.valhalla.clients.driver_client import DriverClient
from src.valhalla.utils.exceptions.unauthorized_user_error import UnauthorizedUserError
from src.valhalla.clients.mysql_client import PyMySqlClient
from src.valhalla.clients.crypto_client import CryptoClient
from src.valhalla.clients.menu_client import MenuClient
from src.valhalla.constants.const import (
    MAX_RETRIES_ALLOWED,
    MASTER_TABLE_NAME,
    HASHED_MASTER_PASSWORD_FIELD_NAME,
    MASTER_FIELD_NAME
)
class TestDriverClient(unittest.TestCase):

    @patch('src.valhalla.clients.mysql_client.PyMySqlClient')
    @patch('src.valhalla.clients.crypto_client.CryptoClient')
    @patch('src.valhalla.clients.crypto_client.CryptoClient.prepare_tools', return_value=None)
    @patch('src.valhalla.clients.menu_client.MenuClient.run', return_value=None)
    def setUp(self, MockPyMySqlClient, MockCryptoClient, MockPrepareTools, MockMenuClientRun):
        self.mock__sql_client = MockPyMySqlClient.return_value
        self.mock__crypto_tools = MockCryptoClient.return_value
        self.secrets = {
            'database_user': 'user',
            'database_password': 'password',
            'host': 'localhost',
            'database': 'test_db',
            'crypto_specs': {
                'odin_username': 'odin',
                'odin_password': 'odin'
            }
        }
        self.project_root = '/mock/project/root'
        self.client = DriverClient(self.secrets, self.project_root)
        self.client._crypto_tools.hash_diff = MagicMock()

    @patch.object(PyMySqlClient, 'database_exists', return_value=False)
    def test_run_database_does_not_exist(self, mock_database_exists):
        with self.assertRaises(ValueError) as context:
            self.client.run()
        self.assertEqual(str(context.exception), "Database 'test_db' does not exist.")
        mock_database_exists.assert_called_once()

    @patch.object(DriverClient, 'validate_input', return_value=('user', 'password'))
    @patch.object(PyMySqlClient, 'database_exists', return_value=True)
    @patch('src.valhalla.clients.menu_client.MenuClient.run', return_value=None)
    def test_run_success(self, mock_database_exists, mock_validate_input, mock_menu_client_run):
        self.client.run()
        mock_validate_input.assert_called_once()
        mock_database_exists.assert_called_once()

    @patch.object(DriverClient, 'validate_input', side_effect=UnauthorizedUserError)
    @patch.object(PyMySqlClient, 'database_exists', return_value=True)
    def test_run_unauthorized_user_error(self, mock_database_exists, mock_validate_input):
        with patch('sys.exit') as mock_exit:
            self.client.run()
            self.assertEqual(mock_validate_input.call_count, MAX_RETRIES_ALLOWED)
            mock_exit.assert_called_once()

    @patch.object(DriverClient, 'get_user_credentials', return_value=('user', 'password'))
    @patch.object(PyMySqlClient, 'retrieve', return_value=[{HASHED_MASTER_PASSWORD_FIELD_NAME: 'hashed_password'}])
    def test_validate_authorized_user_success(self, mock_retrieve, mock_get_user_credentials):
        self.client._crypto_tools.hash_diff.return_value = False
        usr, ps = self.client.validate_input()
        self.assertEqual(usr, 'user')
        self.assertEqual(ps, 'password')
        mock_get_user_credentials.assert_called_once()
        mock_retrieve.assert_called_once_with(MASTER_TABLE_NAME, [HASHED_MASTER_PASSWORD_FIELD_NAME], {MASTER_FIELD_NAME: 'user'})
        self.client._crypto_tools.hash_diff.assert_called_once_with('password', 'hashed_password')

    @patch.object(DriverClient, 'get_user_credentials', return_value=('user', 'password'))
    @patch.object(PyMySqlClient, 'retrieve', return_value=[])
    def test_validate_authorized_user_no_user_found(self, mock_retrieve, mock_get_user_credentials):
        with self.assertRaises(UnauthorizedUserError):
            self.client.validate_input()
        mock_get_user_credentials.assert_called_once()
        mock_retrieve.assert_called_once_with(MASTER_TABLE_NAME, [HASHED_MASTER_PASSWORD_FIELD_NAME], {MASTER_FIELD_NAME: 'user'})

    @patch.object(DriverClient, 'get_user_credentials', return_value=('user', 'password'))
    @patch.object(PyMySqlClient, 'retrieve', return_value=[{HASHED_MASTER_PASSWORD_FIELD_NAME: 'hashed_password'}])
    def test_validate_authorized_user_hash_diff(self, mock_retrieve, mock_get_user_credentials):
        with self.assertRaises(UnauthorizedUserError):
            self.client.validate_input()
        mock_get_user_credentials.assert_called_once()
        mock_retrieve.assert_called_once_with(MASTER_TABLE_NAME, [HASHED_MASTER_PASSWORD_FIELD_NAME], {MASTER_FIELD_NAME: 'user'})
        self.client._crypto_tools.hash_diff.assert_called_once_with('password', 'hashed_password')

    @patch.object(DriverClient, 'get_authorized_creds', return_value=None)
    @patch.object(PyMySqlClient, 'database_exists', return_value=True)
    def test_run_unauthorized_user_error(self, mock_database_exists, mock_get_authorized_creds):
        with self.assertRaises(UnauthorizedUserError):
            self.client.run()
        mock_database_exists.assert_called_once()
        mock_get_authorized_creds.assert_called_once()

if __name__ == '__main__':
    unittest.main()