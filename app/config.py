import os
import logging
from dotenv import load_dotenv

load_dotenv()



class BaseConfig:
    """
    Base Configuration
    """
    # Base
    APP_NAME = os.environ.get('APP_NAME')
    DEBUG = False
    TESTING = False
    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    LOGGING_LOCATION = 'logs/flask.log'
    LOGGING_LEVEL = logging.DEBUG
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY')

class DevelopmentConfig(BaseConfig):
    """
    Development Configuration
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class TestingConfig(BaseConfig):
    """
    Testing Configuration
    """
    # Base
    DEBUG = True
    TESTING = True
    TEST_LOGGING_LEVEL = logging.DEBUG
    TEST_LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    TEST_LOGGING_LOCATION = 'logs/flask_test.log'

    # Config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):
    """
    Production Configuration
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")



config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}