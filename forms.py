from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, TextAreaField, SelectField, PasswordField
from wtforms.validators import InputRequired, Optional, Length, NumberRange, URL, Email


class NewUserForm(FlaskForm):
    """Form for new user to register"""

    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=16)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=16)])
    email = StringField("Email", validators=[Email()])



class EditUserForm(FlaskForm):
    """Form for user to edit profile information"""
    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=16)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=16)])
    zone = SelectField("Hardiness Zone", choices=[('one', 1),('two', 2),('three', 3),('four', 4),('five', 5),('six', 6),('seven', 7),('eight', 8),('nine', 9),('ten', 10),('eleven', 11),('twelve', 12)])
    country = SelectField("Country", validators=[Optional()])
    email = StringField("Email", validators=[Email()])

class LoginForm(FlaskForm):
    """Form to log in user"""

    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=16)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=16)])
