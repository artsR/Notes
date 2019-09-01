from flask import Flask # import the 'Flask' class -
                        # instance of this class will be my 'WSGI Application'.
                        # https://dzone.com/articles/a-detailed-study-of-wsgi-web-server-gateway-interf-1
from flask import escape, url_for
from flask import request # https://flask.palletsprojects.com/en/1.1.x/api/#flask.Request
from flask import render_template # https://jinja.palletsprojects.com/en/2.10.x/templates/
from werkzeug.utils import secure_filename # .filename of uploaded file can be forged so
                                        # never ever trust that value. Instead use 'secure_filename'.


app = Flask(__name__)

"""To start site I need to:
+ run: $env:FLASK_APP = 'app_name.py'
+    : flask run
     : flask run --host=0.0.0.0   # to tell OS to listen on all public IPs.
                                # It means that the server is now public.
                                # Debug mode True allows user execute arbitrary
                                # python code on my computer!"""
# Lets:
## activate debugger,
## activate automatic reloader,
## enable debug mode on Flask application:
#set FLASK_ENV=development # w/o spaces around '='    OR
#$env:FLASK_DEBUG=1  # I can also control debug mode separately from the environment
                    # by exporting FLASK_DEBUG=1

#flask run  # if it doesn't work I used: python -m flask run



@app.route('/') # it tells what URL should trigger 'hello_world' function
def hello_world():
    return 'Hello, World - for the first time with Flask.'

@app.route('/index')
def index():
    return 'Starting page'

"""I can add variable sections to a URL marking sections with '<variable_name>'.
Or I can use a converter to specify the type of the argument '<converter:variable_name>'.

Converters types:
    o) string   - accepts any text w/o a slash
    o) int      - accepts positive integers
    o) float    - accepts positive floating point values
    o) path     - like 'string' but also accepts slashes
    o) uuid     - accepts UUID strings"""

@app.route('/user/<username>')
def show_user_profile(username):
    # Show the user profile for that particular user:
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # Show the post with the given ID, the ID is an integer:
    return f'Post {post_id:d}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # Show the subpath after '/path/':
    return f'Subpath {escape(subpath)}'

# With trailing slash and w/o trailing slash:
@app.route('/projects/') # enter '/projects' and Flask redirect it to '/projects/'
def projects():
    return 'The project page'

@app.route('/about') # type '/about/' cause '404 Not Found Error'
def about():
    return 'The about page'


# URL building:
@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return f'{escape(username)}\'s profile'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))


# HTTP Methods:
"""By default, a route only answers to 'GET' request. I can use the 'methods'
argument of the 'route()' decorator to handle different HTTP methods."""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


# Static files. Generate URLs for static files using the special 'static' endpoint name:
url_for('static', filename='style.css') # now file has to be stored in '/static/style.css'


# Render HTML templates:
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name) # Flask looks for templates
                                                    # in the '/templates/' folder.
"""Inside templates I also have access to the 'request', 'session' and 'g'
as well as the 'get_flashed_message()' function."""

"""Automatic 'escape' is enabled, so if 'name' contains HTML it will be escaped.
If I know it is safe HTML I can mark it as safe by using 'Markup' class or
by using the '|safe' filter in the template."""


# The Request Object: (catching data send by user to the server)
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # Access form data (data send in 'POST' or 'PUT' request):
        if valid_login[request.form['username'], request.form['password']]:
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username or password'
    # Code below will be executed if the request method was 'GET'
    # or the credential were invalid:
    return render_template('login.html', error=error)
""" 'KeyError' will be caught by HTML with '400 Bad Request Error'."""

# To access parameters submitted in the URL (?key=value) I can use 'args' attr:
searchword = request.args.get('key', '') #


# File Uploads:
"""Set the 'enctype="multipart/form-data"' attribute on my HTML form, otherwise
the browser will not transmit my files at all."""
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
         f = request.files['the_file']
         f.save('/var/www/uploads/uploaded_file.txt')
         #f.save('/var/www/uploads/' + secure_filename(f.filename))


# Cookies:
"""To access cookies use 'cookies' attr, to set cookies 'set_cookie'.
To use 'sessions' I should not use 'cookies' directly but instead use 'Sessions'
that add some security on top of the cookies for me."""
@app.route('/')
def index():
    username = request.cookies.get('username')

@app.route('/')
def index():
    resp = make_response(render_template(...)) # create manually 'response' object.
    resp.set_cookie('username', 'the username') # cookies are set on 'response' object.
    return resp


# Redirects and Error (to redirect user to another endpoint):
from flask import abort, redirect, url_for
"""User will be 'redirected' from the index to a page they cannot access
(401 means access denied)."""
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(401) # access denied
    this_is_never_executed()

@app.errorhandler(404) # decorator to customize the error page.
def page_not_found(error):
    return render_template('page_not_found.html'), 404 # '404' tells Flask that the status
                                                    # code of that page should be '404'.


# Responses:
"""The return value from a 'view' function is automatically converted into a response object.
If return value is 'string': converts into 'response' object with 'string' as 'response body'
If return value is 'dict'  : calls 'jsonify()' to produce 'response'."""


#If I want to get hold of the resulting response object inside the 'view' I should use 'make_response':
"""
@app.errorhandler(404):
def not_found(error):
    return render_template('error.html'), 404
"""
@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


# APIs with JSON:
"""If I return a 'dict' from a 'view' then it will be converted to a JSON response."""
@app.route('/me')
def me_api():
    user = get_current_user()
    return {
        'username': user.username,
        'theme': user.theme,
        'image': url_for('user_image', filename=user.image),
    }
"""If I want to create JSON responses for types other than dict I should use 'jsonify()'
that serialize any supported JSON data type"""
@app.route('/users')
def users_api():
    users = get_all_users()
    return jsonify([user.to_json() for user in users])


# Sessions:   ---> session_app.py
"""In addition to the 'request object' there is 'session object'.
It allows me to store information specific to a user from one request to the next.

This is implemented on top of cookies for me and signs the cookies cryptographically.
It means that user can look at the content but cannot modify it, unless
he knows the secret key used for signing."""
from flask import Flask, session, redirect, url_for, escape, request
