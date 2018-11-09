'''
@author: si
'''
from io import BytesIO
import unittest

from prog_image.app import create_app
from prog_image.settings.test_config import Config

SHOW_LOG_MESSAGES = False

if not SHOW_LOG_MESSAGES:
    # hide log messages
    import logging
    logger = logging.getLogger(__name__)
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

    def test_image_upload(self):
        """
        multi-part form mode
        """
        d = {'image': (BytesIO(b"file contents"), 'myfile.jpg') }
        rv = self.test_client.post('/', data=d)
        self.assertEqual(200, rv.status_code)

        # wrong form field name
        d = {'imageX': (BytesIO(b"file contents"), 'myfile.jpg') }
        rv = self.test_client.post('/', data=d)
        self.assertEqual(400, rv.status_code)
