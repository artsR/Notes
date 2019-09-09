import os
basedir = os.path.abspath(os.path.dirname(__file__))

"""Use class to store configuration variables is very good idea.
As the application needs more configuration items, they can be added to this
class, and later if I find that I need to have more than one configuration set,
I can create subclasses of it."""

"""It is in general a good practice to set configuration from environment variables,
and provide a fallback value when the environment does not define the variable.
os.environ.get('variable_name')"""

class Config(object):
    # SECRET_KEY is also used as a cryptographic key to generate signatures or tokens.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'blablabla'
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(basedir, 'microblog.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
