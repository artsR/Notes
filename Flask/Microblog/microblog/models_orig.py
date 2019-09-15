from microblog import app, db
from microblog import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from datetime import datetime
from time import time
import jwt


# Followers assosiation table:
"""This table is not declared as a model, like 'users' and 'posts' tables.
Since this is an auxiliary table that has no data other than 'ForeignKey'."""
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

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
    followed = db.relationship(
    # SQLAlchemy allows to work with 'followed' relationship as if it was a list: user1.followed.append(user2)
                    'User', secondary=followers,
                    primaryjoin=(followers.c.follower_id == id),
                    secondaryjoin=(followers.c.followed_id == id),
                    backref=db.backref('followers', lazy='dynamic'),
                            # The current way of defining 'backref' is better than just 'backref='followers'
                            # because 'backref' created with the 'lazy="dynamic"' returns a query instead of
                            # the final results of the query. It is useful because I can expand the query before
                            # I execute it to obtain the results - e.x. I can ask that the results from the
                            # relationship come sorted in specific way.
                    lazy='dynamic'
                    )


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
                                                                        # is it good practice skip 'self'?
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self,user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
                                # 'filter' is lower level to the 'filter_by'.
                                # 'filter_by' can only check for equality to a constant value.
                                # 'filter' can include arbitrary filtering conditions

    def followed_posts(self):
        followed = Post.query.join(
                followers, (followers.c.followed_id == Post.user_id)
                    # assosiation table
                                # 'join' condition.
            ).filter(followers.c.follower_id == self.id)

        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
                                                        # it's necessary because 'jwt.encode()'
                                                        # returns the token as a byte sequence.
                                                        # In application is more convenient
                                                        # to have token as a string.

    @staticmethod # it means that it can be invoked directly from the class.
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                algorithms=['HS256'])['reset_password'] # if invalid exception raises.
        except:
            return None
        return User.query.get(id)

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
    language = db.Column(db.String(5))
    

    def __repr__(self):
        return f'<Post {self.body}>'


# Flask-Login knows nothing about databases therefore it expects that the
# application will configure a user 'loader function', that can be load a user ID:
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
