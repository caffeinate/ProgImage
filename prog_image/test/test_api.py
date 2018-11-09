'''
@author: si
'''
import json
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
        self.config.reset()
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
        self.assertEqual(201, rv.status_code)

        response = json.loads(rv.data)
        # sha1 of raw string above
        self.assertEqual('034fa2ed8e211e4d20f20e792d777f4a30af1a93',
                         response['id'])

        # correct API response is to give location in header of doc.
        url = None
        for key, value in rv.headers:
            if key == 'Location':
                url = value
                break

        self.assertTrue(url.endswith('/images/{}/'.format(response['id'])))


    def test_wrong_form_field_name(self):
        # wrong form field name
        d = {'imageX': (BytesIO(b"file contents"), 'myfile.jpg') }
        rv = self.test_client.post('/', data=d)
        self.assertEqual(400, rv.status_code)
        
