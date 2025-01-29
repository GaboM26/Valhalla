import unittest
from unittest.mock import patch, MagicMock
from src.valhalla.clients.driver_client import DriverClient
from src.valhalla.utils.exceptions.unauthorized_user_error import UnauthorizedUserError
from src.valhalla.clients.mysql_client import PyMySqlClient
from src.valhalla.clients.crypto_client import CryptoClient
from src.valhalla.constants.const import (
    MAX_RETRIES_ALLOWED,
    MASTER_TABLE_NAME,
    HASHED_MASTER_PASSWORD_FIELD_NAME,
    MASTER_FIELD_NAME
)
class TestDriverClient(unittest.TestCase):

    @patch('src.valhalla.clients.mysql_client.PyMySqlClient')
    @patch('src.valhalla.clients.crypto_client.CryptoClient')
    def setUp(self, MockPyMySqlClient, MockCryptoClient):
        self.mock_sql_client = MockPyMySqlClient.return_value
        self.mock_crypto_tools = MockCryptoClient.return_value
        self.secrets = {
            'database_user': 'user',
            'database_password': 'password',
            'host': 'localhost',
            'database': 'test_db'
        }
        self.client = DriverClient(self.secrets)
        self.client.crypto_tools.hash_diff = MagicMock()

    @patch.object(PyMySqlClient, 'database_exists', return_value=False)
    def test_run_database_does_not_exist(self, mock_database_exists):
        with self.assertRaises(ValueError) as context:
            self.client.run()
        self.assertEqual(str(context.exception), "Database 'test_db' does not exist.")
        mock_database_exists.assert_called_once()

    @patch.object(DriverClient, 'validate_authorized_user', return_value=('user', 'password'))
    @patch.object(DriverClient, 'display_menu')
    @patch.object(PyMySqlClient, 'database_exists', return_value=True)
    def test_run_success(self, mock_database_exists, mock_validate_authorized_user, mock_display_menu):
        self.client.run()
        mock_validate_authorized_user.assert_called_once()
        mock_display_menu.assert_called_once()
        mock_database_exists.assert_called_once()

    @patch.object(DriverClient, 'validate_authorized_user', side_effect=UnauthorizedUserError)
    @patch.object(PyMySqlClient, 'database_exists', return_value=True)
    def test_run_unauthorized_user_error(self, mock_database_exists, mock_validate_authorized_user):
        with patch('sys.exit') as mock_exit:
            self.client.run()
            self.assertEqual(mock_validate_authorized_user.call_count, MAX_RETRIES_ALLOWED)
            mock_exit.assert_called_once()

    @patch.object(DriverClient, 'get_user_credentials', return_value=('user', 'password'))
    @patch.object(PyMySqlClient, 'retrieve', return_value=[{HASHED_MASTER_PASSWORD_FIELD_NAME: 'hashed_password'}])
    def test_validate_authorized_user_success(self, mock_retrieve, mock_get_user_credentials):
        self.client.crypto_tools.hash_diff.return_value = False
        usr, ps = self.client.validate_authorized_user()
        self.assertEqual(usr, 'user')
        self.assertEqual(ps, 'password')
        mock_get_user_credentials.assert_called_once()
        mock_retrieve.assert_called_once_with(MASTER_TABLE_NAME, [HASHED_MASTER_PASSWORD_FIELD_NAME], {MASTER_FIELD_NAME: 'user'})
        self.client.crypto_tools.hash_diff.assert_called_once_with('password', 'hashed_password')

    @patch.object(DriverClient, 'get_user_credentials', return_value=('user', 'password'))
    @patch.object(PyMySqlClient, 'retrieve', return_value=[])
    def test_validate_authorized_user_no_user_found(self, mock_retrieve, mock_get_user_credentials):
        with self.assertRaises(UnauthorizedUserError):
            self.client.validate_authorized_user()
        mock_get_user_credentials.assert_called_once()
        mock_retrieve.assert_called_once_with(MASTER_TABLE_NAME, [HASHED_MASTER_PASSWORD_FIELD_NAME], {MASTER_FIELD_NAME: 'user'})

    @patch.object(DriverClient, 'get_user_credentials', return_value=('user', 'password'))
    @patch.object(PyMySqlClient, 'retrieve', return_value=[{HASHED_MASTER_PASSWORD_FIELD_NAME: 'hashed_password'}])
    def test_validate_authorized_user_hash_diff(self, mock_retrieve, mock_get_user_credentials):
        with self.assertRaises(UnauthorizedUserError):
            self.client.validate_authorized_user()
        mock_get_user_credentials.assert_called_once()
        mock_retrieve.assert_called_once_with(MASTER_TABLE_NAME, [HASHED_MASTER_PASSWORD_FIELD_NAME], {MASTER_FIELD_NAME: 'user'})
        self.client.crypto_tools.hash_diff.assert_called_once_with('password', 'hashed_password')

if __name__ == '__main__':
    unittest.main()