from flask import Flask, render_template, redirect, flash, url_for, g, jsonify, session
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Plan
from forms import NewUserForm, LoginForm, EditUserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///garden_planner'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.debug = True
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
    """Shows homepage and recent garden plans"""

    plans = Plan.query.first()
    
    return render_template('home.html')
    # return render_template('base.html')

@app.route('/register', methods=["GET", "POST"])
def signup():
    """Shows and handles form to sign up new user"""

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

            do_login(user)

            return redirect('/')
        
        except IntegrityError:
            flash("Username already taken","danger")
            return render_template('/users/register.html')
        
    return render_template('/users/register.html', form=form)
        
@app.route('/login', methods=["GET", "POST"])
def login():
    """Shows and handles form to login"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")
    
        flash("Invalid credentials.", 'danger')
        return redirect('/login')
    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    do_logout()
    return redirect('/')

@app.route('/user/<int:user_id>')
# Should show user's public plans, also private plans if user's own profile, show profile information (except email), and have a link to edit profile information if it is the user's own profile

@app.route('/user/<int:user_id>/edit', methods=["GET", "POST"])
def edit_profile(user_id):
    """Shows and handles form for user to edit profile"""

    form = EditUserForm
    user = User.query.get(user_id)

    form.data.username = user.username
    form.data.email = user.email
    form.data.zone = user.zone
    # if 

    flash('Profile Updated!')
    return redirect(f'/user/{user_id}')
# Show EditForm to allow user to edit profile information