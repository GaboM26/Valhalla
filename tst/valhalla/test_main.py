import unittest
from src.valhalla.main import main
from unittest.mock import patch, MagicMock
from pymysql.err import OperationalError
from src.valhalla.utils.exceptions.unauthorized_user_error import UnauthorizedUserError

class TstNamespace:
        
    def __init__(self, secrets):
        self.secrets = 'TEST'

class TestMain(unittest.TestCase):
    @patch('src.valhalla.main.DriverClient')
    @patch('src.valhalla.main.ValhallaConfigParser')
    def test_main(self, MockValhallaConfigParser, MockDriverClient):

        mock_parser_instance = MockValhallaConfigParser.return_value
        mock_parser_instance.get_secrets.return_value = 'mock_secrets'
        
        mock_driver_instance = MockDriverClient.return_value
        
        args = TstNamespace(secrets='TEST')
        project_root = '/mock/project/root'  # Mock project root
        with patch('src.valhalla.main.project_root', project_root):
            main(args)
        
        MockValhallaConfigParser.assert_called_once_with('TEST')
        mock_parser_instance.get_secrets.assert_called_once()
        MockDriverClient.assert_called_once_with('mock_secrets', project_root)
        mock_driver_instance.run.assert_called_once()

        if __name__ == "__main__":
            unittest.main()

    @patch('src.valhalla.main.DriverClient')
    @patch('src.valhalla.main.ValhallaConfigParser')
    def test_operational_error_handling(self, MockValhallaConfigParser, MockDriverClient):
        # Mock the ValhallaConfigParser to return a mock secrets dictionary
        mock_parser_instance = MockValhallaConfigParser.return_value
        mock_parser_instance.get_secrets.return_value = {
            'database_user': 'user',
            'database_password': 'password',
            'host': 'localhost',
            'database': 'test_db'
        }

        # Mock the DriverClient to raise an OperationalError when run is called
        mock_driver_instance = MockDriverClient.return_value
        mock_driver_instance.run.side_effect = OperationalError

        # Capture the output
        with self.assertLogs(level='ERROR') as log:
            args = TstNamespace(secrets='TEST')
            retval = main(args)
            self.assertEqual(retval, -1)

        # Check that the error message was logged
        self.assertIn("OperationalError", log.output[0])
        @patch('src.valhalla.main.DriverClient')
        @patch('src.valhalla.main.ValhallaConfigParser')
        def test_unauthorized_user_error_handling(self, MockValhallaConfigParser, MockDriverClient):
            # Mock the ValhallaConfigParser to return a mock secrets dictionary
            mock_parser_instance = MockValhallaConfigParser.return_value
            mock_parser_instance.get_secrets.return_value = {
                'database_user': 'user',
                'database_password': 'password',
                'host': 'localhost',
                'database': 'test_db'
            }

            # Mock the DriverClient to raise an UnauthorizedUserError when run is called
            mock_driver_instance = MockDriverClient.return_value
            mock_driver_instance.run.side_effect = UnauthorizedUserError

            # Capture the output
            with self.assertLogs(level='ERROR') as log:
                with self.assertRaises(SystemExit):  # Assuming main exits on error
                    args = TstNamespace(secrets='TEST')
                    main(args)

            # Check that the error message was logged
            self.assertIn("UnauthorizedUserError", log.output[0])
    


if __name__ == "__main__":
    unittest.main()