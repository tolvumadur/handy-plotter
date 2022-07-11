import unittest
import os, sys

HERE = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(HERE,'..','src'))
from hp import HandyPlotter

class TestInit(unittest.TestCase):
    def test_empty_init(self):
        a =  HandyPlotter()
        self.assertIsNotNone(a)
        self.assertFalse(hasattr(a, "config"))
    
    def test_config_init(self):
        a = HandyPlotter(os.path.join(HERE, "static", "test_config.json"))
        self.assertIsNotNone(a)
        self.assertTrue(hasattr(a, "config"))
        self.assertRaises(Exception, HandyPlotter, *["NoSuchPathExists"])

    def test_bad_init(self):
        self.assertRaises(Exception, HandyPlotter, *["a", "b", 2])
        self.assertRaises(Exception, HandyPlotter, *[os.path.join(HERE, "static", "test_config.json"), None])


if __name__ == '__main__':
    unittest.main()