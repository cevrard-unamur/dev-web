from flask_wtf import FlaskForm
from wtforms   import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import ValidationError, InputRequired, Length, Email, EqualTo
from app.models.user import User

import datetime

def birtday_check(form, field):
        if field.data >= datetime.date.today():
            raise ValidationError('Votre date de naissance doit être dans le passé')

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
    passwordConfirm = PasswordField('Confirmation du mot de passe', validators=[
        EqualTo('password',
            message='Les mots de passe ne correspondent pas'
        )])
    firstname = StringField('Prénom', validators=[
        InputRequired(
            message='Le prénom est requis'
        )])
    lastname = StringField('Nom', validators=[
        InputRequired(
            message='Le nom est requis'
        )])
    birthday = DateField('Date de naissance', format='%d/%m/%Y', validators=[
        InputRequired(
            message='La date de naissance est requise'
        ), birtday_check])
    email = StringField('Email', validators=[
        InputRequired(
            message='L\'email est requis'
        ), 
        Email(
            message='L\'adresse entrée n\'est pas correcte'
        )])
    submit   = SubmitField('S\'inscrire')

    