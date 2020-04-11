from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id              = db.Column(db.Integer, primary_key=True)
    username        = db.Column(db.String(80), unique=True, nullable=False)
    password_hash   = db.Column(db.String(128), nullable=False)
    firstname       = db.Column(db.String(40), nullable=False)
    lastname        = db.Column(db.String(40), nullable=False)
    birthday        = db.Column(db.DateTime(), nullable=False)
    email           = db.Column(db.String(60), nullable=False)
    accountLevel    = db.Column(db.Integer, nullable=False, default=0)
    tasks           = db.relationship('Task', backref='author', lazy='dynamic')

    def __init__(self, username, firstname, lastname, birthday, email, accountLevel):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.birthday = birthday
        self.email = email
        self.accountLevel = accountLevel

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "username = %s, email = %s" % (self.username, self.email)