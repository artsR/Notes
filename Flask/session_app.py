"""In addition to the 'request object' there is 'session object'.
It allows me to store information specific to a user from one request to the next.

This is implemented on top of cookies for me and signs the cookies cryptographically.
It means that user can look at the content but cannot modify it, unless
he knows the secret key used for signing."""
from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
#python -c 'import os; print(os.urandom(16))'
app.secret_key = b'\xd3\xef\xaa!?\xa4\xec\x1f/\xeb_,\x03\xda\xdd\xef'

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return """
        <form method='post'>
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    """

@app.route('/logout')
def logout():
    # remove the username from the session if it's there:
    session.pop('username', None)
    return redirect(url_for('index'))


# Message Flashing:  -- >  flash_app.py
"""Using 'flash()' method I can record message at the end of a request and access it
on the next (and only the next) request."""


# Logging:
app.logger.debug('A value for debugging')
app.logger.warning('A warning occured (%d apples)', 42)
app.logger.error('An error occured')


# Hooking in 'WSGI Middlewares':
"""I want to add a 'WSGI Middleware' to my application I can wrap the internal 'WSGI' application.
Ex. to use one of the middleware from 'werkzeug' package to work around bugs in 'lighttpd':"""
from werkzeug.contrib.fixers import LighttpdCGIRootFix
app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)


# Extensions: ex. SQZAlchemy or support for sending email, REST API...
"""
from flask_foo import Foo

foo = Foo()

app = Flask(__name__)
app.config.update(
    FOO_BAR='baz',
    FOO_SPAM='eggs'
)

foo.init_app(app)
"""

if __name__ == '__main__':
    app.run(debug=True)
