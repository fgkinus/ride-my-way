import os

from werkzeug.contrib.cache import SimpleCache


class Config(object):
    """Parent settings file"""

    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing"""

    Testing = True
    DEBUG = True


class StagingConfig(Config):
    """Configurations for staging"""

    DEBUG = False


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
#  a cache to store session dat while server is running
CACHE = SimpleCache()  # simple cache to store session data.

