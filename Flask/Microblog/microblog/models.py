from datetime import datetime
from microblog import db
from microblog import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # 'posts' field is not an actual database field, but a high-level view of the
    # relationship between users and posts. This field runs query, so:
    # 'user_name.posts' returns all the posts written by that user.
    posts = db.relationship('Post', backref='author', lazy='dynamic') # 'Post' refers to name of class.
                                    # defines the name of a field that will be added to
                                    # the objects of the 'many' class that points back at
                                    # the 'one' object. This adds 'post.author' expression
                                    # that returns the user given a post.


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?id=identicos&s={size}'
                                                                        # is it good practice skip 'self'?
    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
                                        # 'index=True' field is going to be indexed,
                                        # that is useful if I want to retrieve posts in chronological order.
                                        # (I don't understand why)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 'user.id': 'user' is name of table.
                                                            # A model is given by its database table name,
                                                            # for which SQLAlchemy automatically uses lowercase
                                                            # characters and, for multi-word model names,
                                                            # snake case (snake_case).

    def __repr__(self):
        return f'<Post {self.body}>'


# Flask-Login knows nothing about databases therefore it expects that the
# application will configure a user 'loader function', that can be load a user ID:
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
