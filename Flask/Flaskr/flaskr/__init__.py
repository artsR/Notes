import os
from flask import Flask


def create_app(test_config=None):
    # Create and configure the app:
    app = Flask(__name__, instance_relative_config=True) # creates Flask instance.
                # name of current Python module
                            # relative to the instance folder (outside the 'flaskr' package - security reasons)
    app.config.from_mapping(
        SECRET_KEY='dev', # this value should be replace to random one when deploying.
        DATABASE=os.path.join(app.instance_path, 'flaskr_sqlite'),
                                    # instance_path refers to path where Flask instance is (instance folder).
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing:
        app.config.from_pyfile('config.py', silent=True)
                    # Overrides the default configuration with the values taken from the 'config.py'
                    # in the instance folder if it exists.
                    # Ex. it can be used to set a real 'SECRET_KEY' when deploying.
    else:
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists:
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # A simple page that says hello to user:
    @app.route('/hello')
    def hello():
        return 'Hello, sir!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
