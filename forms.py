from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, TextAreaField, SelectField, PasswordField, SelectMultipleField
from wtforms.validators import InputRequired, Optional, Length, NumberRange, URL, Email
from country_list import country_list
from wtforms_alchemy import QuerySelectMultipleField


class NewUserForm(FlaskForm):
    """Form for new user to register"""

    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=16)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=16)])
    email = StringField("Email", validators=[Email()])

class EditUserForm(FlaskForm):
    """Form for user to edit profile information"""
    
    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=16)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=16)])
    zone = SelectField("Hardiness Zone", choices=[('1', 1),('2', 2),('3', 3),('4', 4),('5', 5),('6', 6),('7', 7),('8', 8),('9', 9),('10', 10),('11', 11),('12', 12)], coerce=int)
    country = SelectField("Country", validate_choice=False, coerce=str)
    # choices=[(1,'afghanistan')],
    email = StringField("Email", validators=[Email()])

class LoginForm(FlaskForm):
    """Form to log in user"""

    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=16)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=16)])

class NewPlanForm(FlaskForm):
    """Form to create a new plan"""

    title = StringField("Title", validators=[InputRequired()])
    private = BooleanField("Make Private?")

class AddToPlanForm(FlaskForm):
    """Form to select which plans to add a selected plant"""

    plans = SelectMultipleField("plans", validate_choice=False, coerce=int)