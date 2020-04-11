from flask_wtf import FlaskForm
from wtforms   import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Length, Email, EqualTo
from app.models.user import User

class LoginForm( FlaskForm ):
    username = StringField('Nom d\'utilisateur', validators=[
        InputRequired(
            message='Le nom d\'utilisateur est requis'
        ), 
        Length(
            min=2, 
            max =80,
            message='Le nom d\'utilisateur doit être compris entre 2 et 80 caractères'
        )])
    password = PasswordField('Mot de passe', validators=[
        InputRequired(
            message='Le mot de passe est requis'
        ), 
        Length(
            min=5, 
            max=16,
            message='Le mot de passe doit être compris entre 5 et 16 caractères'
        )])
    submit   = SubmitField('Se connecter')