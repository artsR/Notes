import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
                # 'g' is a special object that is unique for each 'request'.
                # Stores data that might be accessed by multiple functions during the 'request'.
                # The 'connection' is stored and reused instead of creating a new one
                # if 'get_db' is called second time in the same 'request'.
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
                # another special object that points to the 'Flask application' handling the 'request'.
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
                            # tells the 'connection' to returns row like dict.

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
                        # open a file relative to the 'flaskr' package.
        db.executescript(f.read().decode('utf-8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# Does registration of 'close_db' and 'init_db_command' to make using it possible.
# However, since I am using a 'factory function', that instance isn't available now.
# So instead, I put 'registration' into a function that takes 'application' and does registr.:
def init_app(app):
    app.teardown_appcontext(close_db)
        # tells Flask to call that function when 'cleaning up' after returning 'response'.
    app.cli.add_command(init_db_command)
        # adds a new command that can be called with the 'flask' 'command'.
