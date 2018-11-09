'''
@author: si
'''
from flask import Blueprint, request

from prog_image.utils import JsonException

general_bp = Blueprint('views', __name__)

@general_bp.route('/', methods=['POST'])
def index():
    
    # multi-part form mode
    if 'image' not in request.files:
        msg = ("Missing data: Image uploads should be in multi-part forms "
               "with the image data being named 'image'")
        raise JsonException(msg)

    uploaded_file = request.files['image']
    return "Hello world"
