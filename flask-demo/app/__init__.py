from flask import Flask
from werkzeug.exceptions import HTTPException
import settings
import app.models as models
from environs import Env

env = Env()
env.read_env()

def register_blueprint(app: Flask):
    from app.api.basic import api as basic_api
    from app.api.v1 import api as api_v1
    app.register_blueprint(api_v1, url_prefix='/v1')
    app.register_blueprint(basic_api, url_prefix='/basic')

def register_error_handler(app: Flask):
    @app.errorhandler(Exception)
    def framework_error(e):
        from app.api.common.error import APIException
        from app.api.common.resp import ServerError, NotFoundError, UnsupportedMethod

        if isinstance(e, APIException):
            return e
        elif isinstance(e, HTTPException):
            code = e.code
            msg = e.description
            error_code = 3000
            if code == 404:
                return NotFoundError()
            elif code == 405:
                return UnsupportedMethod()
            return APIException(error_code, msg, None)

        # 未知错误
        app.logger.exception(e)
        if app.config['DEBUG']:
            raise e
        return ServerError()

def register_plugin(app: Flask):
    from flask_cors import CORS
    CORS(app, supports_credentials=True)

def register_logger(app: Flask):
    """注册日志规则"""
    from app.utils.logger import file_logger
    file_logger.init_app(app)

def create_app():
    env = Env()
    env.read_env()
    run_env = env.str('RUN_ENV') if env.str('RUN_ENV') else 'production'

    app = Flask(__name__)

    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')
    app.config.from_object(settings.configs[run_env])
    app.config['SQLALCHEMY_DATABASE_URI'] = env.str('DATABASE_URI')

    models.init(app)

    register_blueprint(app)
    register_error_handler(app)
    register_plugin(app)
    register_logger(app)

    return app