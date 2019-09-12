"""'View functions': are mapped to one or more route URLs so that Flask knows
what logic to execute when a client 'requests' a given URL."""

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from microblog import app, db
from microblog.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from microblog.forms import ResetPasswordRequestForm, ResetPasswordForm
from microblog.models import User, Post
from microblog.email import send_password_reset_email
from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    form = PostForm()

    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post was sent succesfully!')
        return redirect(url_for('index'))
                #TODO make explanation why redirect instead of render_template...
                #because of refreshing issue in the browser.. bla...bla...blabla...
                #trick: POST/Redirect/GET pattern... To avoid inserting duplicate
                #posts when a user refreshes the page after submitting a web form.

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], 0)
    next_url = ( url_for('index', page=posts.next_num)
        if posts.has_next else None )
    prev_url = ( url_for('index', page=posts.prev_num)
        if posts.has_prev else None )

    return render_template('index.html', form=form, posts=posts.items,
                        next_url=next_url, prev_url=prev_url)


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
    page = request.args.get('page', 1, type=int)
    posts = ( user.posts.order_by(Post.timestamp.desc())
        .paginate(page, app.config['POSTS_PER_PAGE'], False) )
    next_url = ( url_for('user', username=user.username, page=posts.next_num)
        if posts.has_next else None )
    prev_url = ( url_for('user', username=user.username, page=posts.prev_num)
        if posts.has_prev else None )

    return render_template('user.html', user=user, posts=posts.items,
                    next_url=next_url, prev_url=prev_url)


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

@app.route('/explore')
#@login_required
def explore():
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.timestamp.desc()).paginate(
                page, app.config['POSTS_PER_PAGE'], False)
        next_url = ( url_for('explore', page=posts.next_num)
            if posts.has_next else None )
        prev_url = ( url_for('explore', page=posts.prev_num)
            if posts.has_prev else None )

        return render_template('index.html', posts=posts.items,
                            next_url=next_url, prev_url=prev_url)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User {username} not found.')
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself.')
        return redirect(url_for('index'))
    current_user.follow(user)
    db.session.commit()
    flash(f'You are following {username}!')
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User {username} not found.')
        return redirect(url_for('index'))
    if user == current_user:
        flash(f'You cannot unfollow yourself.')
        return redirect(url_for('index'))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You are not following {username}')
    return redirect(url_for('user', username=username))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            send_password_reset_email(user)
        flash('Check you email for the instructions to reset your password')
        return redirect(url_for('login'))

    return render_template('reset_password_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been changed.')
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form)


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
