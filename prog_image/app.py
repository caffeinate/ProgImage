'''
@author: si
'''
from flask import Flask

from prog_image.utils import JsonException, handle_json_exception


def create_app(settings_class):
    app = Flask(__name__)
    app.config.from_object(settings_class)

    app.register_error_handler(JsonException, handle_json_exception)
    app.register_error_handler(500, handle_json_exception)

    from prog_image.views import general_bp
    app.register_blueprint(general_bp)

    return app


if __name__ == '__main__':
    app = create_app('prog_image.settings.local_config.Config')
    app.run(debug=app.config['DEBUG'], use_reloader=True, port=5070)
