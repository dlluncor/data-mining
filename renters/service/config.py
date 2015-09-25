import os

DEFAULT_MIXPANEL_TOKEN = 'c1642a350ca7177a2bd888a1db8e7cf4'
DEFAULT_GA_TOKEN = 'UA-66635208-3'
DEFAULT_MONGODB_URI = "mongodb://127.0.0.1"

class Config:
    mongodb_uri = DEFAULT_MONGODB_URI
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

    forms = [('MidQ',  'https://davidl.typeform.com/to/zl1h8F', 1),
             ('Short', 'https://davidl.typeform.com/to/YrYEjW', 1),
             ('Long',  'https://davidl.typeform.com/to/KIwzWC', 1)]
    weighted_forms = [(name, val) for name, val, cnt in forms for i in range(cnt)]

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TEST = True

class ProductionConfig(Config):
    PROD = True
    mongodb_uri = os.environ.get('MONGOLAB_URI')

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
