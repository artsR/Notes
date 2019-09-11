"""'View functions': are mapped to one or more route URLs so that Flask knows
what logic to execute when a client 'requests' a given URL."""

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from microblog import app, db
from microblog.forms import LoginForm, RegistrationForm, EditProfileForm
from microblog.models import User
from datetime import datetime


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', posts=posts)


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

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
            # Registers the user as logged in, so that means that any future pages
            # the user navigates to will have the 'current_user' variable set to that user.
            # In the previous Blog it was resolved with 'session.set_cookies' and 'g.user'.
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
                                # Prevent unsecure behaviour like inserting a URL
                                # to the a malicious site in the 'next' variable.
                                # So the application only redirects when the URL is relative.
                                                    # 'netloc' is a domain part of URL.
                                                    # From https://tools.ietf.org/html/rfc1808.html#section-2.1
                                                    # every URL should follow a specific format:
                                                    # <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
                                                    # (what about 3rd party sites that allow shorten URL?)
            next_page = url_for('index')

        flash(f'POST method used. - user {u}, remember_me={r}, password={p}')
        flash(f'POST method used. - user {user, user.email, user.id}')
        return redirect(next_page)

    flash(f'{form.errors}')
    flash(f'GET method used.')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You Signed Up succesfully. Now you can login to our service.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():

    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@app.before_request # Executing a bit of generic logic ahead of a request being dispatched
                # to a view function is such a common task in web applications that
                # Flask offers it as a native feature ('@app.before_request').
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        # In this point I don't need 'db.session.add()' because when I reference
        # 'current_user', Flask-Login invokes user loader callback function '@login.user_loader'
        # 'load_user' which runs a database query that puts the target user in the database session.
        # So I don't need to add the user again in this function because it is already there.
        db.session.commit()
