import os

_user = os.environ.get('POSTGRES_USER')
_password = os.environ.get('POSTGRES_PASSWORD')
_host = os.environ.get('POSTGRES_HOST')
_database = os.environ.get('POSTGRES_DB')
_port = os.environ.get('POSTGRES_PORT')


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')

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
