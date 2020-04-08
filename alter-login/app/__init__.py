from flask import Flask

from config import Config
app = Flask(__name__)
app.config.from_object(Config)

from flask_login import LoginManager
login_manager = LoginManager( app )
login_manager.login_view = "login"
login_manager.login_message_category = "info"
login_manager.login_message = "You can not access this page. Please log in to access this page."

from app import routes
