import unittest
from unittest.mock import patch, MagicMock
from src.valhalla.clients.driver_client import DriverClient
from src.valhalla.clients.mysql_client import PyMySqlClient
from src.valhalla.utils.exceptions.unauthorized_user_error import UnauthorizedUserError

class TestDriverClient(unittest.TestCase):

    @patch('src.valhalla.clients.mysql_client.PyMySqlClient')
    def setUp(self, MockPyMySqlClient):
        self.mock_sql_client = MockPyMySqlClient.return_value
        self.secrets = {
            'database_user': 'user',
            'database_password': 'password',
            'host': 'localhost',
            'database': 'test_db'
        }
        self.client = DriverClient(self.secrets)

    @patch.object(PyMySqlClient, 'database_exists', return_value=False)
    def test_run_database_does_not_exist(self, mock_database_exists):
        with self.assertRaises(ValueError) as context:
            self.client.run()
        self.assertEqual(str(context.exception), "Database 'test_db' does not exist.")
        mock_database_exists.assert_called_once()

    @patch.object(DriverClient, 'validate_authorized_user')
    @patch.object(DriverClient, 'display_menu')
    @patch.object(PyMySqlClient, 'database_exists', return_value=True)
    def test_run_success(self, mock_execute_menu, mock_validate_authorized_user, mock_database_exists):
        self.client.run()
        mock_validate_authorized_user.assert_called_once()
        mock_execute_menu.assert_called_once()
        mock_database_exists.assert_called_once()

    @patch.object(DriverClient, 'validate_authorized_user', side_effect=UnauthorizedUserError)
    @patch.object(PyMySqlClient, 'database_exists', return_value=True)
    def test_run_unauthorized_user_error(self, mock_validate_authorized_user, mock_database_exists):
        with patch('builtins.print') as mocked_print:
            self.client.run()
            mocked_print.assert_called_with("Username/Password Incorrect")

    @patch.object(DriverClient, 'validate_authorized_user', side_effect=Exception("Some error"))
    @patch.object(PyMySqlClient, 'database_exists', return_value=True)
    def test_run_unknown_exception(self, mock_validate_authorized_user, mock_database_exists):
        with patch('builtins.print') as mocked_print:
            self.client.run()
            mocked_print.assert_called_with("Unknown Exception occured: Some error")

if __name__ == '__main__':
    unittest.main()