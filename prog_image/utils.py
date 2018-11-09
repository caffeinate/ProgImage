'''
@author: si
'''
from flask import current_app, jsonify, request
from flask import url_for as url_for_flask

class JsonException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, system_message=None):
        """
        @param status_code: integer
        """
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

        if self.status_code >= 500:
            current_app.logger.error(message)

        if self.status_code >= 400 and self.status_code != 404:
            if system_message:
                current_app.logger.warning("Client error: "+system_message)
            else:
                current_app.logger.warning("Client error: "+message)

    def to_dict(self):
        """
        close enough to Google Errors.
        """
        rv = { 'error': { 'message' : self.message } }
        return rv


def handle_json_exception(error):
    if hasattr(error, 'to_dict') and hasattr(error, 'status_code'):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    elif hasattr(error, 'message'):
        response = jsonify({'msg': error.message})
        return response, 500
    else:
        response = jsonify({'msg': 'Unknown error'})
        return response, 500

def url_for(*args, **kwargs):
    """
    wrap normal flask url_for and use config['PREFERRED_URL_SCHEME'] but
    without requiring config to have APPLICATION_ROOT & SERVER_NAME
    """
    if '_external' not in kwargs:
        return url_for_flask(*args, **kwargs)
    #print "schema:"+request.environ.get('HTTP_X_SCHEME', "unknown")
    forced_scheme = request.environ.get('HTTP_X_SCHEME',
                                        current_app.config.get('PREFERRED_URL_SCHEME'))
     
    return url_for_flask(*args, _scheme=forced_scheme, **kwargs)
