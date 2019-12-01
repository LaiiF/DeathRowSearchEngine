from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

#Login Form that users can log in from the cloud stored website.
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
#Input for the text search
class TextSearchForm(FlaskForm):
    lastwords = StringField('Last Words')
    submit = SubmitField('Search')

    def __repr__(self):
        return f"Last Words('{self.lastwords}')"

