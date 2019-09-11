from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate # 'Flask-Migrate' uses 'Alembic' migration framework.
from flask_login import LoginManager


app = Flask(__name__)
#app.config['SECRET_KEY'] = b"\x10p\r]\xec\xf7\xb8\xf5\x80t\xd1U\xc5A;'"
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'  # 'login' value is the function (endpoint) name for the login view.
                            # (why I have to add this?) - because 'Flask-Login' needs to know
                            # what is the view function that handles logins.
                            # (I don't understand. what 'login_view' does? Is it responsible for
                            # redirecting to the login page if user NOT LOGGED IN?)


from microblog import routes
from microblog import models # defines the structure of the database.
from microblog import errors

#-------------------------------------------------------------------------------
## Sending server error notification via email :
import logging
from logging.handlers import SMTPHandler

if not app.debug: # Enable 'email logger' if application is running w/o 'debug' mode.
    if app.config['MAIL_SERVER']: # Enable 'email logger' if 'email server' exists in the configuration.

        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr=f"no-reply@{app.config['MAIL_SERVER']}",
            toaddrs=app.config['ADMINS'],
            subject='Microblog Failure',
            credentials=auth,
            secure=secure,
        )

        mail_handler.setLevel(logging.ERROR)

        app.logger.addHandler(mail_handler) # Add 'mail_handler' to the application.


## Sending server error notification to file:
import os
from logging.handlers import RotatingFileHandler

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs\\microblog.log',
                                    maxBytes=10240,
                                    backupCount=10 # keeps last 10 'log' files.
                                    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
    )

    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

#-------------------------------------------------------------------------------

# # To use 'flask shell' w/o need of importing everytime 'User', 'Post' and 'db'
# from microblog.models import User, Post
# @app.shell_context_processor
# def make_shell_context():
#     return { 'db': db, 'User': User, 'Post': Post }
