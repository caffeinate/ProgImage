'''
@author: si
'''
from io import BytesIO
import json
import os
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
        sample_file_contents = "file contents"
        d = {'image': (BytesIO(bytes(sample_file_contents, 'ascii')), 'myfile.jpg') }
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

        # ensure it was written to disk
        file_on_disk = self.config.FILEBASE+'/0/3/'+response['id']
        with open(file_on_disk) as f:
            file_contents = f.read()
        
        self.assertEqual(sample_file_contents, file_contents)

    def test_wrong_form_field_name(self):
        # wrong form field name
        d = {'imageX': (BytesIO(b"file contents"), 'myfile.jpg') }
        rv = self.test_client.post('/', data=d)
        self.assertEqual(400, rv.status_code)
        

    def test_generate_thumbnail(self):
        """
        upload a read image and download the thumbnail
        """
        sample_image_file = os.path.abspath(os.path.dirname(__file__)+'/sample_data/diver.jpeg')
        with open(sample_image_file, 'rb') as f:
            d = {'image': (BytesIO(f.read()), 'diver.jpeg') }

        rv = self.test_client.post('/', data=d)
        self.assertEqual(201, rv.status_code)
        response = json.loads(rv.data)

        # should/could use http Location header
        url = '/images/{}/thumbnail/'.format(response['id'])
        rv = self.test_client.get(url)
        self.assertEqual(200, rv.status_code)
        # not checking the actual image

    def test_on_demand_thumbnail(self):
        """
        image uploaded and result downloaded in single request. Nothing stored server side
        """
        sample_image_file = os.path.abspath(os.path.dirname(__file__)+'/sample_data/diver.jpeg')
        with open(sample_image_file, 'rb') as f:
            d = {'image': (BytesIO(f.read()), 'diver.jpeg') }

        rv = self.test_client.post('/on_demand/thumbnail/', data=d)
        self.assertEqual(200, rv.status_code)

        # not checking image, just number of bytes
        self.assertEqual(3378, len(rv.data))
