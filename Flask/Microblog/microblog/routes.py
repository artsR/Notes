"""'View functions': are mapped to one or more route URLs so that Flask knows
what logic to execute when a client 'requests' a given URL."""

from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from microblog import app
from microblog.forms import LoginForm
from microblog.models import User


@app.route('/')
@app.route('/index')
@app.route('/user/')
@app.route('/user/<username>')
def index(username='my friend'):
    return render_template('index.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    u = form.username.data
    p = form.password.data
    r = form.remember_me.data

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user in None or not user.check_password(form.password.data):
            flash('Invalid username or password')
        login_user(user, remember=form.remember_me.data)
            # Registers the user as logged in, so that means that any future pages
            # the user navigates to will have the 'current_user' variable set to that user.
            # In the previous Blog it was resolved with 'session.set_cookies'.
        flash(f'POST method used. - user {u}, remember_me={r}')
        flash(f'POST method used. - user {user}')
        return redirect(url_for('index'))

    flash(f'{form.errors}')
    flash(f'GET method used.')

    return render_template('login.html', form=form)
