from flask_wtf import FlaskForm
from wtforms   import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Length, Email, EqualTo
from app.models import User, Short_messages

class MyLoginForm( FlaskForm ):
    username = StringField('Username:', validators=[InputRequired(), Length(min=5, max=80)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=3, max=16)])
    submit   = SubmitField('Login')



class MyRegistrationForm(FlaskForm):
    username  = StringField('Username:', validators=[InputRequired(), Length(min=5, max=80)])
    email     = StringField('Email', validators=[InputRequired(), Email()])
    password  = PasswordField('Password:', validators=[InputRequired(), Length(min=3, max=16)])
    password2 = PasswordField('Repeat Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


        
class ShortMessageForm( FlaskForm ):
    text     = StringField('Leave your short message here:', validators=[InputRequired(), Length(min=0, max=200)])
    submit   = SubmitField('Send')
