from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    password      = db.Column(db.String(16))
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    s_message     = db.relationship('Short_messages', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return "username = %s, email = %s" % (self.username, self.email)

    
class Short_messages(db.Model):

    __tablename__ = 'short_messages'

    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text          = db.Column(db.String(200))
    time_stamp    = db.Column(db.DateTime, index=True, default=datetime.utcnow )
    users_id      = db.Column(db.Integer, db.ForeignKey('users.id') )

    def __repr__(self):
        return '< Shot message >'.format(self.text)
    
db.drop_all()
db.create_all()

from app import login_manager

# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))
