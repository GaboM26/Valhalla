import unittest
from src.valhalla.utils.payload_builder import PayloadBuilder
from src.valhalla.constants.const import (
    SECRETS_TABLE_NAME,
    APPNAME_FIELD,
    USERNAME_FIELD,
    PASSWORD_FIELD,
    VALHALLA_USERNAME_FIELD
)

class TestPayloadBuilder(unittest.TestCase):

    def setUp(self):
        self.builder = PayloadBuilder()

    def test_build_returns_correct_function(self):
        build_func = self.builder.build(SECRETS_TABLE_NAME)
        self.assertEqual(build_func, self.builder.build_secret_entry)

    def test_build_secret_entry(self):
        app_name = 123
        username = 456
        password = 789
        valhalla_username = "test_user"
        expected_payload = {
            APPNAME_FIELD: app_name,
            USERNAME_FIELD: username,
            PASSWORD_FIELD: password,
            VALHALLA_USERNAME_FIELD: valhalla_username
        }
        payload = self.builder.build_secret_entry(app_name, username, password, valhalla_username)
        self.assertEqual(payload, expected_payload)

    def test_get_encrypted_columns(self):
        encrypted_columns = self.builder.get_encrypted_columns(SECRETS_TABLE_NAME)
        expected_columns = [APPNAME_FIELD, USERNAME_FIELD, PASSWORD_FIELD]
        self.assertEqual(encrypted_columns, expected_columns)

    def test_build_raises_not_implemented_error_for_unrecognized_table(self):
        with self.assertRaises(NotImplementedError):
            self.builder.build("unknown_table")

    def test_get_encrypted_columns_raises_not_implemented_error_for_unrecognized_table(self):
        with self.assertRaises(NotImplementedError):
            self.builder.get_encrypted_columns("unknown_table")

if __name__ == "__main__":
    unittest.main()