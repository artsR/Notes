from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate # 'Flask-Migrate' uses 'Alembic' migration framework.
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel # 404.html and 500.html translated only.



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
# login.login_message = 'Please log in to access this page'
                            # This message is generated as default by 'Flask-Login' extension when
                            # user w/o login tries access page that '@login_required'.
                            # Now, I may change the message which will be displayed.
                            # I could translate it: _l('above message bla bla bla').
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app) # info: 404.html and 500.html translated only


from microblog import routes
from microblog import models # defines the structure of the database.
from microblog import errors


# Text translation: only in informational purpose.------------------------------
@babel.localeselector
def get_locale(): # this decorated function is invoked for each request to select a language translation.
    return request.accept_languages.best_match(app.config['LANGUAGES'])
                    # 'request' attribute that provides high-level interface to work with 'Accept-Language' header:
                                                                                            # the content of this
                                                                                            # header can be configured
                                                                                            # by user in the browser's
                                                                                            # preferences page.
                                                                                            # The default is usually
                                                                                            # imported from the
                                                                                            # language settings in the
                                                                                            # computer's OS.
                    # (Accept-Language: da, en-gb;q=0.8, en;q=0.7) - prefered Danish w/ weight 1, en-gb w/ weight 0.7..
                    # that clients send with a request: specifies the client language settings in the computer's OS.


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
