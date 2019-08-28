from flask import Flask # import the 'Flask' class -
                        # instance of this class will be my 'WSGI Application'.
                        # https://dzone.com/articles/a-detailed-study-of-wsgi-web-server-gateway-interf-1


app = Flask(__name__)

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
