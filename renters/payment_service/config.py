import os

DEFAULT_MONGODB_URI = "mongodb://127.0.0.1"
DEFAULT_PRIVATE_KEY_PATH = "test_private_key.pem"
DEFAULT_PUBLIC_KEY_PATH = "test_public_key.pem"

class Config:
    DEBUG, PROD, TEST = False, False, False
    mongodb_uri = DEFAULT_MONGODB_URI
    private_key_path = DEFAULT_PRIVATE_KEY_PATH
    public_key_path = DEFAULT_PUBLIC_KEY_PATH

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TEST = True

class ProductionConfig(Config):
    PROD = True

    mongodb_uri = os.environ.get('MONGODB_URI') or DEFAULT_MONGODB_URI
    private_key_path = os.environ.get('PRIVATE_KEY_PATH') or DEFAULT_PRIVATE_KEY_PATH
    public_key_path = os.environ.get('PUBLIC_KEY_PATH') or DEFAULT_PUBLIC_KEY_PATH

envs = {
    'TEST': TestingConfig,
    'PROD': ProductionConfig,
    'DEFAULT': DevelopmentConfig
}

env_name = os.environ.get('APP_ENV', 'DEFAULT')
config =  envs[env_name] if env_name in envs else envs['DEFAULT']
