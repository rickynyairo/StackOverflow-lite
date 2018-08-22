"""
This module sets the configurations for the application

"""
import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY", "kalongo")
    DATABASE_URL="dbname='stackoverflow-lite' host='localhost'\
                 port='5432' user='rickynyairo' password='aces4890'"

class DevelopmentConfig(Config):
    """Development phase configurations"""
    DEBUG = True

class TestingConfig(Config):
    """Testing Configurations."""
    TESTING = True
    DEBUG = True

class ReleaseConfig(Config):
    """Release Configurations."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'release': ReleaseConfig,
}