import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Parent settings file"""

    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    TESTING = False
    DATABASE_NAME = os.getenv('DB_NAME')
    DATABASE_USER = os.getenv('DB_USER')
    DATABASE_PASSWORD = os.getenv('DB_PASSWORD')


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True



class TestingConfig(Config):
    """Configurations for Testing"""

    TESTING = True
    DATABASE_NAME = os.getenv('TESTING_DB_NAME')
    DATABASE_USER = os.getenv('TESTING_DB_USER')
    DATABASE_PASSWORD = os.getenv('TESTING_DB_PASSWORD')


class StagingConfig(Config):
    """Configurations for staging"""

    DEBUG = True
    DEVELOPMENT = True


class ProductionConfig(Config):
    """Configurations for Production."""

    DEBUG = False
    TESTING = False


APP_CONFIG = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
