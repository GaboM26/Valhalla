import unittest
from src.valhalla.main import main
from unittest.mock import patch, MagicMock

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
        main(args)
        
        MockValhallaConfigParser.assert_called_once_with('TEST')
        mock_parser_instance.get_secrets.assert_called_once()
        MockDriverClient.assert_called_once_with('mock_secrets')
        mock_driver_instance.run.assert_called_once()

        if __name__ == "__main__":
            unittest.main()


    


if __name__ == "__main__":
    unittest.main()