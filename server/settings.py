
import config


class BaseConfig:
    """ Basic settings required by all classes """
    SECRET_KEY = config.SECRET_KEY
    MAIL_SERVER = 'smtp.gmail.com'
    # TESTING = True
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = config.SENDER_EMAIL
    MAIL_PASSWORD = config.PASSWORD
    MAIL_DEFAULT_SENDER = config.SENDER_EMAIL
    MAIL_DEBUG = config.DEBUG

    # Flask
    DEBUG = config.DEBUG


class TestingConfig(BaseConfig):
    """ Testing settings  """
    TESTING = True
