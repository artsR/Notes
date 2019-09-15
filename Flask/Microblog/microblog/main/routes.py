"""'View functions': are mapped to one or more route URLs so that Flask knows
what logic to execute when a client 'requests' a given URL."""

from datetime import datetime
from guess_language import guess_language
from flask import render_template, flash, redirect, url_for, request, g
from flask import current_app, jsonify
from flask_login import current_user, login_required
from flask_babel import get_locale
from microblog import db
from microblog.main import bp
from microblog.main.forms import EditProfileForm, PostForm
from microblog.models import User, Post
from microblog.translate import translate



@bp.before_request # Executing a bit of generic logic ahead of a request being dispatched
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

    # Configuration of localization (prefered language):
    g.locale = str(get_locale())
                    # decorated ('@babel.localeselector') function returning
                    # selected language and locale for a given request.
      # adding it to the 'g' object I can access it from the 'base' template:
      # 'moment.lang(g.locale)' adding to the 'block scripts'.



@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    form = PostForm()

    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash('Your message was posted succesfully!')
        return redirect(url_for('main.index'))
                #TODO make explanation why redirect instead of render_template...
                #because of refreshing issue in the browser.. bla...bla...blabla...
                #trick: POST/Redirect/GET pattern... To avoid inserting duplicate
                #posts when a user refreshes the page after submitting a web form.

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], 0)
    next_url = ( url_for('main.index', page=posts.next_num)
        if posts.has_next else None )
    prev_url = ( url_for('main.index', page=posts.prev_num)
        if posts.has_prev else None )

    return render_template('index.html', form=form, posts=posts.items,
                        next_url=next_url, prev_url=prev_url)


@bp.route('/explore')
#@login_required
def explore():
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.timestamp.desc()).paginate(
                page,current_app.config['POSTS_PER_PAGE'], False)
        next_url = ( url_for('main.explore', page=posts.next_num)
            if posts.has_next else None )
        prev_url = ( url_for('main.explore', page=posts.prev_num)
            if posts.has_prev else None )

        return render_template('index.html', posts=posts.items,
                            next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = ( user.posts.order_by(Post.timestamp.desc())
        .paginate(page, current_app.config['POSTS_PER_PAGE'], False) )
    next_url = ( url_for('main.user', username=user.username, page=posts.next_num)
        if posts.has_next else None )
    prev_url = ( url_for('main.user', username=user.username, page=posts.prev_num)
        if posts.has_prev else None )

    return render_template('user.html', user=user, posts=posts.items,
                    next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():

    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User {username} not found.')
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot follow yourself.')
        return redirect(url_for('main.index'))
    current_user.follow(user)
    db.session.commit()
    flash(f'You are following {username}!')
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User {username} not found.')
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(f'You cannot unfollow yourself.')
        return redirect(url_for('main.index'))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You are not following {username}')
    return redirect(url_for('main.user', username=username))


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    """'jsonify' returns HTTP Response object."""
    return jsonify({'text': translate(
                                request.form['text'],
                                request.form['source_language'],
                                request.form['dest_language']
                                )# 'request.form' in this case will be sent to this function by JS.
    # outcome: translated text - is in form of HTTP Response object (client can get it by 'response['text']').
})
