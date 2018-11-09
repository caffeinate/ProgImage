'''
Simplify running coverage tests by linking to all unit test from one python
file.
@author: si
'''
import unittest

from prog_image.test.test_api import ApiTest

if __name__ == "__main__":
    unittest.main()
