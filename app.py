from flask import Flask, render_template, redirect, flash, url_for, g, jsonify, session
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User
from forms import NewUserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///garden_planner'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ihaveasecret'
app.app_context().push()

curr_user = "curr_user"

connect_db(app)
db.create_all()

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if curr_user in session:
        g.user = User.query.get(session[curr_user])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[curr_user] = user.id


def do_logout():
    """Logout user."""

    if curr_user in session:
        del session[curr_user]

@app.route('/')
def homepage():
    return render_template('base.html')

@app.route('/register', methods=["GET", "POST"])
def signup():
    """Shows form to sign up new user"""

    form = NewUserForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
                username = form.username.data,
                password = form.password.data,
                email = form.email.data
            )
            db.session.add(user)
            db.session.commit()

            return render_template("base.html")
        
        except IntegrityError:
            flash("Username already taken","danger")
            return render_template('register.html')