import json
import traceback
from logging.config import dictConfig

from flask import Flask
from dotenv import load_dotenv

import extensions.celery
import extensions.sqlalchemy


def create_app(name):
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'default'
        }},
        'root': {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    })
    flask_app = Flask(name)
    load_dotenv()
    flask_app.config.from_prefixed_env()
    flask_app.url_map.strict_slashes = False
    register_extensions(flask_app)

    @flask_app.errorhandler(Exception)
    def on_error(e):
        flask_app.logger.error(f'Error: {e}\n{traceback.format_exc()})')
        return str(e), 500

    from fibonacci.views import bp
    flask_app.register_blueprint(bp)

    return flask_app


def register_extensions(app):
    extensions.sqlalchemy.db.init_app(app)
    with app.app_context():
        print(extensions.sqlalchemy.db.engine)
    extensions.celery.init_celery(app)
