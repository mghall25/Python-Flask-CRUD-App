# app/__init__.py

import os

# third-party imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

# local imports
from config import app_config

# initialization
db = SQLAlchemy()
login_manager = LoginManager()

# based on config name, load correct config.py file
def create_app(config_name):
    # added - if else
    if os.getenv('FLASK_CONFIG') == "production":
      app = Flask(__name__)
      app.config.update(
            SECRET_KEY=os.getenv('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
        )
    else:
      app = Flask(__name__, instance_relative_config=True)
      app.config.from_object(app_config[config_name])
      app.config.from_pyfile('config.py')
    
    Bootstrap(app)
    db.init_app(app)
	
	# initialize LoginManager object, add view and message
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
	
    # migration object
    migrate = Migrate(app, db)

	# import models from app
    from app import models
	
	# import and register blueprints
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

	# aadded - error handler
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500
	
    return app