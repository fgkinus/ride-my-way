import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Parent settings file"""

    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    TESTING = False
    DATABASE_NAME = None
    DATABASE_USER = 'postgres'
    DATABASE_PASSWORD = ''


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    DATABASE_NAME = 'rmw'


class TestingConfig(Config):
    """Configurations for Testing"""

    TESTING = True
    DATABASE_NAME = 'testing'


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
