class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True

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