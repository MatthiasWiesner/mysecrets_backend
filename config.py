class BaseConfig(object):
    DEBUG = False
    TESTING = False
    ORATOR_DATABASES = {
        'default': 'development',
        'development': {
            'driver': 'postgres',
            'database': 'mysecrets',
            'host': 'localhost',
            'user': 'mysecret',
            'password': 'mysecrets',
        },
        'production': {
            'driver': 'postgres',
            'database': 'mysecrets',
            'host': 'localhost',
            'user': 'mysecret',
            'password': 'mysecrets',
        }
    }

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    KEY = 'OPCKgemRoM6EoZU8'


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = True
