from flask_wtf import FlaskForm
from wtforms   import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

class MyLoginForm( FlaskForm ):
    username = StringField('Username:', validators=[InputRequired(), Length(min=5, max=10)])
    password = PasswordField('Password:', validators=[Length(min=12, max=12)])
    submit   = SubmitField('Send')
