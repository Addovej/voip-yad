import os

_user = os.environ.get('POSTGRES_USER')
_password = os.environ.get('POSTGRES_PASSWORD')
_host = os.environ.get('POSTGRES_HOST')
_database = os.environ.get('POSTGRES_DB')
_port = os.environ.get('POSTGRES_PORT')


class Config(object):
    """
    Main application config.
    """

    FLASK_ADMIN_SWATCH = 'cerulean'

    SECRET_KEY = os.environ.get('SECRET_KEY')

    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = 'ATGUOHAELKiubahiughaerGOJAEGj'
    SECURITY_URL_PREFIX = '/admin'

    SECURITY_LOGIN_URL = '/login/'
    SECURITY_LOGOUT_URL = '/logout/'
    SECURITY_REGISTER_URL = '/register/'

    SECURITY_POST_LOGIN_VIEW = '/admin/'
    SECURITY_POST_LOGOUT_VIEW = '/admin/'
    SECURITY_POST_REGISTER_VIEW = '/admin/'

    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False

    SESSION_TYPE = 'filesystem'
    SWAGGER = {
        'specs': [
            {
                'version': '0.0.1',
                'title': 'VOIP Intergation Emulation',
                'endpoint': 'v1_spec',
                'route': '/v1/spec',
            }
        ],
        'components': {
            'securitySchemes': {
                'ApiKeyAuth': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'Token'
                },
                'apiKey': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'Token'
                }
            }
        },
        'securityDefinitions': {
            'apiKey': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Token'
            }
        }
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
        _user,
        _password,
        _host,
        _port,
        _database
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    YA_DISK_APP_ID = os.environ.get('YA_DISK_APP_ID')
    YA_DISK_APP_SECRET = os.environ.get('YA_DISK_APP_SECRET')
    YA_DISC_BASE_FOLDER = os.environ.get('YA_DISC_BASE_FOLDER')
