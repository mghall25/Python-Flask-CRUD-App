# config.py

class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments
	
    DEBUG=True


class DevelopmentConfig(Config):
    """
    Development configurations
	SQLAlchemy config vars - http://flask-sqlalchemy.pocoo.org/2.1/config/
    """
    # TESTING = True
	# environment var FLASK_DEBUG=1 necessary
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

	
class TestingConfig(Config):
    """
    Testing configurations
    """

    TESTING = True

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
	'testing': TestingConfig
}