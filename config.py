import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

class TwitterConfig(object):
    CONSUMER_KEY = 'somekey'
    CONSUMER_SECRET = 'somesecret'
    ACCESS_TOKEN = 'sometoken'
    ACCESS_TOKEN_SECRET = 'sometokensecret'

