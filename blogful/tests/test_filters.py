import os
import unittest
import datetime
import json
import sys

# Set python path to root blogful dir so I can import blog
sys.path.append(os.path.dirname(__file__)+"/../")

# print(sys.path)

# Configure app to use the testing configuration
if not "CONFIG_PATH" in os.environ:
    os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

# import blog
from blog.filters import *

class FilterTests(unittest.TestCase):
    """ Unit tests """
    def test_date_format(self):
        # Tonight we're gonna party
        date = datetime.date(1999, 12, 31)
        formatted = dateformat(date, "%y/%m/%d")
        self.assertEqual(formatted, "99/12/31")

    def test_date_format_none(self):
        formatted = dateformat(None, "%y/%m/%d")
        self.assertEqual(formatted, None)

if __name__ == '__main__':
    unittest.main()