import unittest
from src.valhalla.utils.misc import int_str_to_bytes

class TestMisc(unittest.TestCase):

    def test_int_str_to_bytes_little_endian(self):
        int_str = "12345"
        the_number = 12345
        expected_bytes = the_number.to_bytes((the_number.bit_length() + 7) // 8, byteorder='little')
        result = int_str_to_bytes(int_str, byteorder='little')
        self.assertEqual(result, expected_bytes)

    def test_int_str_to_bytes_big_endian(self):
        int_str = "12345"
        the_number = 12345
        expected_bytes = the_number.to_bytes((the_number.bit_length() + 7) // 8, byteorder='big')
        result = int_str_to_bytes(int_str, byteorder='big')
        self.assertEqual(result, expected_bytes)

    def test_int_str_to_bytes_zero(self):
        int_str = "0"
        the_number = 0
        expected_bytes = the_number.to_bytes((the_number.bit_length() + 7) // 8, byteorder='little')
        result = int_str_to_bytes(int_str, byteorder='little')
        self.assertEqual(result, expected_bytes)

    def test_int_str_to_bytes_negative(self):
        int_str = "-12345"
        with self.assertRaises(OverflowError):
            int_str_to_bytes(int_str, byteorder='little')

    def test_int_str_to_bytes_invalid_input(self):
        int_str = "abc"
        with self.assertRaises(ValueError):
            int_str_to_bytes(int_str, byteorder='little')

if __name__ == "__main__":
    unittest.main()