'''
@author: si
'''
import unittest

from prog_image.app import create_app
from prog_image.settings.test_config import Config

SHOW_LOG_MESSAGES = False

if not SHOW_LOG_MESSAGES:
    # hide log messages
    import logging
    logger = logging.getLogger('prog_image.app')
    logger.setLevel(logging.CRITICAL)

class ApiTest(unittest.TestCase):

    def setUp(self):
        self.config = Config()
        self.app = create_app(self.config)
        self.test_client = self.app.test_client()

    def tearDown(self):
        pass

    def log(self, msg):
        if SHOW_LOG_MESSAGES:
            print(msg)

    def test_root(self):
        """
        top level root can have images POSTed to it.
        GET isn't permitted.
        """
        rv = self.test_client.get('/')
        self.assertEqual(405, rv.status_code) # 405 Method Not Allowed

        rv = self.test_client.post('/', data={})
        self.assertEqual(200, rv.status_code)
        self.assertIn(b'Hello world', rv.data)
