from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, TextAreaField, SelectField, PasswordField
from wtforms.validators import InputRequired, Optional, Length, NumberRange, URL, Email


class NewUserForm(FlaskForm):
    """Form for new user to register"""

    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=16)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=16)])
    zone = SelectField("Hardiness Zone", choices=[((1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12))], coerce=int)
    country = SelectField("Country", validators=[Optional()])
    email = StringField("Email", validators=[Email()])

# class EditUserForm(FlaskForm):
#     """Form for user to edit profile information"""

class LoginForm(FlaskForm):
    """Form to log in user"""
    
    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=16)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=16)])
