'''
@author: si
'''
import hashlib
from tempfile import NamedTemporaryFile

from flask import Blueprint, request, current_app, jsonify, send_file

from prog_image.utils import JsonException, url_for
from prog_image.control.file_base_filesystem import FileBaseFilesystem
from prog_image.control.image_anvil import ImageAnvil

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

    file_storage = FileBaseFilesystem(current_app.config['FILEBASE'])
    file_storage.stored_file = ident

    if not file_storage.file_exists():
        raise JsonException("File not found", status_code=404)

    # TODO mimetype=fsm.mime_type,
    return send_file(file_storage.stored_location,
                     mimetype='image/jpeg',
                     as_attachment=False,
                     attachment_filename=file_storage.meta_data['file_name'])

@general_bp.route('/images/<ident>/<transform_name>/')
def transform_image(ident, transform_name):
    """
    Transform an image already uploaded.

    see :class:`prog_image.control.image_anvil.ImageAnvil` for available
    transforms.
    """
    file_storage = FileBaseFilesystem(current_app.config['FILEBASE'])
    file_storage.stored_file = ident

    if not file_storage.file_exists():
        raise JsonException("File not found", status_code=404)

    image_anvil = ImageAnvil()
    if not image_anvil.is_valid_transform(transform_name):
        raise JsonException("Unknown transform type")

    transformed_image = file_storage.variant_stored_location(transform_name)
    if not file_storage.file_exists(transform_name=transform_name):
        # not already on disk so build it
        current_app.logger.info("Transforming image")
        image_anvil.transform(transform_name,
                              file_storage.stored_location,
                              transformed_image
                              )
    else:
        current_app.logger.info("Using cached image")

    # TODO mimetype=fsm.mime_type,
    suggested_name = file_storage.meta_data['file_name']+'_'+transform_name
    return send_file(transformed_image,
                     mimetype='image/jpeg',
                     as_attachment=False,
                     attachment_filename=suggested_name)

@general_bp.route('/on_demand/<transform_name>/', methods=['POST'])
def on_demand(transform_name):
    """
    POST and image directly to a transform. No files are stored,
    transformed image is in the response.
    """
    # multi-part form mode
    if 'image' not in request.files:
        msg = ("Missing data: Image uploads should be in multi-part forms "
               "with the image data being named 'image'")
        raise JsonException(msg)

    uploaded_file = request.files['image']

    image_anvil = ImageAnvil()
    if not image_anvil.is_valid_transform(transform_name):
        raise JsonException("Unknown transform type")


    transformed_file = NamedTemporaryFile()

    current_app.logger.info("Transforming on demand image")
    image_anvil.transform(transform_name,
                          uploaded_file.stream,
                          transformed_file
                          )

    # transformed file will be cleaned up after garbage collection

    # TODO mimetype=fsm.mime_type,
    suggested_name = transform_name
    transformed_file.flush()
    transformed_file.seek(0)
    return send_file(transformed_file,
                     mimetype='image/jpeg',
                     as_attachment=False,
                     attachment_filename=suggested_name)
