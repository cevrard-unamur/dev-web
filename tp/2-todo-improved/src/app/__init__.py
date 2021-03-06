from flask import Flask
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import routes

from app import login_manager
from app.models.user import User

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))