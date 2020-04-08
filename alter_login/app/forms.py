from flask_wtf import FlaskForm
from wtforms   import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

class MyLoginForm( FlaskForm ):
    username = StringField('Username:', validators=[InputRequired(), Length(min=5, max=20)])
    password = PasswordField('Password:', validators=[Length(min=3, max=16)])
    submit   = SubmitField('Send')
