import unittest
import os
from src.valhalla.utils.parser import ValhallaConfigParser

class TestValhallaConfigParser(unittest.TestCase):

    def setUp(self):
        # Create a temporary secrets.yaml file for testing
        self.test_secrets_path = 'test_secrets.yaml'
        with open(self.test_secrets_path, 'w') as file:
            file.write("key: value\n")

    def tearDown(self):
        # Remove the temporary secrets.yaml file after tests
        if os.path.exists(self.test_secrets_path):
            os.remove(self.test_secrets_path)

    def test_get_secrets_file_exists(self):
        parser = ValhallaConfigParser(self.test_secrets_path)
        secrets = parser.get_secrets()
        self.assertEqual(secrets['key'], 'value')

    def test_get_secrets_file_not_found(self):
        parser = ValhallaConfigParser('non_existent_secrets.yaml')
        with self.assertRaises(FileNotFoundError):
            parser.get_secrets()

if __name__ == '__main__':
    unittest.main()