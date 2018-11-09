'''
@author: si
'''
from flask import Blueprint

general_bp = Blueprint('views', __name__)

@general_bp.route('/', methods=['POST'])
def index():
    return "Hello world"
