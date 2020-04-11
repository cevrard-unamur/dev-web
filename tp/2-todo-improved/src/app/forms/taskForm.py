from flask_wtf import FlaskForm
from wtforms   import StringField, DateField, SubmitField, TextAreaField, HiddenField, validators
from wtforms.validators import ValidationError, InputRequired, Length, Email, EqualTo
from app.models.user import User

class TaskForm( FlaskForm ):
    id          = HiddenField('id')
    title       = StringField('Title', validators=[
        InputRequired(
            message='Le title de la tâche est requis'
        ), 
        Length(
            min=1, 
            max =50,
            message='Le title de la tâche doit être compris entre 1 et 50 caractères'
        )])
    description = TextAreaField('Description')
    due_date    = DateField('Échéance', format='%d/%m/%Y', validators=[validators.Optional()])
    submit      = SubmitField('Sauvegader')