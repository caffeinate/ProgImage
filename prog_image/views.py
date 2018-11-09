'''
@author: si
'''
import hashlib

from flask import Blueprint, request, current_app, jsonify

from prog_image.utils import JsonException, url_for
from prog_image.control.file_base_filesystem import FileBaseFilesystem

general_bp = Blueprint('api_views', __name__)

@general_bp.route('/', methods=['POST'])
def index():
    
    # multi-part form mode
    if 'image' not in request.files:
        msg = ("Missing data: Image uploads should be in multi-part forms "
               "with the image data being named 'image'")
        raise JsonException(msg)

    uploaded_file = request.files['image']
    
    # TODO - check legality of file (type, maybe extension)
    
    # could use secure_filename() but this is a simple way to make URL
    # safe filenames
    sha1_hash = hashlib.sha1(uploaded_file.stream.read()).hexdigest()

    file_storage = FileBaseFilesystem(current_app.config['FILEBASE'])
    file_storage.stored_file = sha1_hash

    if file_storage.file_exists():
        # TODO this is wrong, should tell user base url for the file
        raise JsonException("Duplicate file")

    file_storage.meta_data = {'file_name': uploaded_file.filename}
    file_storage.save(uploaded_file)

    api_url = url_for('api_views.raw_image',
                      ident=file_storage.stored_file,
                      _external=True)

    d = {'msg': 'ok',
         'id': file_storage.stored_file,
         }
    response = jsonify(d)
    response.headers["Location"] = api_url
    return response, 201

    return file_storage.stored_file

@general_bp.route('/images/<ident>/')
def raw_image(ident):
    pass
