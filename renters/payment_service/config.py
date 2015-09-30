import os

DEFAULT_MONGODB_URI = "mongodb://127.0.0.1"

class Config:
    DEBUG, PROD, TEST = False, False, False
    mongodb_uri = DEFAULT_MONGODB_URI

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TEST = True

class ProductionConfig(Config):
    PROD = True

    mongodb_uri = os.environ.get('MONGODB_URI') or DEFAULT_MONGODB_URI

envs = {
    'TEST': TestingConfig,
    'PROD': ProductionConfig,
    'DEFAULT': DevelopmentConfig
}

env_name = os.environ.get('APP_ENV', 'DEFAULT')
config =  envs[env_name] if env_name in envs else envs['DEFAULT']
