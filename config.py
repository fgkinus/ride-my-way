import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Parent settings file"""

    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing"""

    TESTING = True


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
