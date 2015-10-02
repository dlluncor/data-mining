import os

DEFAULT_MIXPANEL_TOKEN = 'c1642a350ca7177a2bd888a1db8e7cf4'
DEFAULT_GA_TOKEN = 'UA-66635208-3'
DEFAULT_MONGODB_URI = "mongodb://127.0.0.1"
DEFAULT_PAYMENT_ENDPOINT = "http://127.0.0.1:8888/credit_cards"
DEFAULT_PUBLIC_KEY_PATH = "../payment_service/keys/test_public_key.pem"

def get_key(key_path):
    with open(key_path, 'r') as fin:
        key = fin.read()
        return key.replace("\n", '')

class Config:
    DEBUG, PROD, TEST = False, False, False

    mongodb_uri = DEFAULT_MONGODB_URI
    payment_endpoint = DEFAULT_PAYMENT_ENDPOINT
    public_key = get_key(DEFAULT_PUBLIC_KEY_PATH)

    sendgrid_username = 'app40814311@heroku.com'
    sendgrid_password = 'dczhilw36273'
    enable_send_email = True

    social = {
        'fb': 'https://www.facebook.com/kainoadevice',
        'linkedin': 'https://angel.co/kainoa',
        'twitter': 'https://twitter.com/kainoa_devices',
    }

    pages = {
        'tos': '/tos',
        'privacy_policy': '/privacy_policy',
    }

    apis = {
        'mixpanel_token': DEFAULT_MIXPANEL_TOKEN,
        'ga_token': DEFAULT_GA_TOKEN,
    }

    # Whether to use the memorized model only when showing prices to the
    # user.
    use_memorized_only = True


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TEST = True

class ProductionConfig(Config):
    PROD = True

    mongodb_uri = os.environ.get('MONGOLAB_URI') or DEFAULT_MONGODB_URI
    payment_endpoint = "http://172.31.26.118/credit_cards"
    public_key = get_key(os.environ.get('PUBLIC_KEY_PATH') or DEFAULT_PUBLIC_KEY_PATH)

    apis = {
        'mixpanel_token': os.environ.get('MIXPANEL_TOKEN') or DEFAULT_MIXPANEL_TOKEN,
        'ga_token': os.environ.get('DEFAULT_GA_TOKEN') or DEFAULT_GA_TOKEN,
    }

envs = {
    'TEST': TestingConfig,
    'PROD': ProductionConfig,
    'DEFAULT': DevelopmentConfig
}

env_name = os.environ.get('APP_ENV', 'DEFAULT')
config =  envs[env_name] if env_name in envs else envs['DEFAULT']
