import unittest
from src.valhalla.utils.hash_pass import *

class TestMain(unittest.TestCase):
    def test_main(self):
        self.assertEqual(main(), None)

if __name__ == "__main__":
    unittest.main()