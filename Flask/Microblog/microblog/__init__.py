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


from microblog import routes
from microblog import models # defines the structure of the database.


# # To use 'flask shell' w/o need of importing everytime 'User', 'Post' and 'db'
# from microblog.models import User, Post
# @app.shell_context_processor
# def make_shell_context():
#     return { 'db': db, 'User': User, 'Post': Post }
