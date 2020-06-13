from chemovar import db
from flask_security import UserMixin, RoleMixin

# The many-to-many helper table
# to relate Role and User models.
roleusers = db.Table(
    'role_users',
    db.Column(
        'user_id', db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True,

    ),
    db.Column(
        'role_id', db.Integer,
        db.ForeignKey('role.id'),
        primary_key=True,

    )
)


class Role(db.Model, RoleMixin):
    '''
    A way to associate permissions with a 
    group of users. For instance: Editor, Admin, or
    Superuser.
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    '''
    The user model which will undergo authentication.
    The UserMixin adds several methods from the
    Flask-Login package, which is included with Flask-
    Security.
    '''
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255))
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
