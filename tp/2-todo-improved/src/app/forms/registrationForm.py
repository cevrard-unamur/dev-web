from flask_wtf import FlaskForm
from wtforms   import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import ValidationError, InputRequired, Length, Email, EqualTo
from app.models.user import User

class RegistrationForm( FlaskForm ):
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
    firstname = StringField('Prénom', validators=[
        InputRequired(
            message='Le prénom est requis'
        )])
    lastname = StringField('Nom', validators=[
        InputRequired(
            message='Le nom est requis'
        )])
    birthday = DateField('Date de naissance', validators=[
        InputRequired(
            message='La date de naissance est requise'
        )])
    email = StringField('Email', validators=[
        InputRequired(
            message='L\'email est requis'
        ), 
        Email(
            message='L\'adresse entrée n\'est pas correcte'
        )])
    submit   = SubmitField('S\'inscrire')