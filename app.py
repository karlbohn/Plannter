from flask import Flask, render_template, redirect, flash, url_for, g, jsonify, session, request
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Plan, PlantRole
from forms import NewUserForm, LoginForm, EditUserForm, AddToPlanForm, NewPlanForm
from country_list import country_list
from pdb import set_trace
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///garden_planner'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.debug = True
app.config['SECRET_KEY'] = 'ihaveasecret'
app.app_context().push()
api_key = 'sk-Zvqe65ee8f14d45554522'
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

    plans = Plan.query.order_by(Plan.id.desc()).limit(5).all()
    
    return render_template('home.html', plans=plans)    

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

### User section - Handles User viewing/adding/editing profiles, viewing user's plans 
@app.route('/users')
def users():
    """No option to view list of users. Redirects to home."""
    return redirect('/')

@app.route('/users/<int:user_id>')
def show_profile(user_id):

    user = User.query.get(user_id)
    plans = Plan.query.filter_by(owner_id=user_id).limit(5).all()

    return render_template("/users/show.html", user=user, plans=plans)

@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_profile(user_id):
    """Shows and handles form for user to edit profile"""
    
    user = User.query.get(user_id)
    if g.user.id == user.id:

        form = EditUserForm()

        form.username.data = user.username
        form.email.data = user.email
        form.country.choices =[(country) for country in country_list]
        if user.zone:
            form.zone.data = user.zone
        if user.country:
            form.country.data = user.country
        

        if form.validate_on_submit():
            user = User.authenticate(form.username.data, form.password.data)

            if user:
                user.username = form.username.data
                user.email = form.email.data
                user.zone = form.zone.data
                user.country = form.country.data

                db.session.add(user)
                db.session.commit()

                flash('Profile Updated!')
                return redirect(f'/users/{user_id}')
       
    else:
        flash("Access denied.")
        redirect("/")    
    return render_template('/users/edit.html', form=form)


@app.route('/users/<int:user_id>/plans')
def show_user_plans(user_id):
    """Shows a list of a given user's plans"""

    plans = Plan.query.filter_by(owner_id=user_id).all()
    user = g.user

    return render_template('/plans/list.html', plans=plans, user=user)

### Plan section
@app.route('/plans')
def show_plans():
    """Shows list of first 20 public garden plans"""

    plans = Plan.query.filter_by(private = False).order_by(Plan.id.desc()).limit(20).all()

    return render_template("/plans/index.html", plans=plans, page_num=1)

@app.route('/plans/page/<int:page_num>')
def next_page_plan(page_num):
    """Shows additional pages of public plans, newest first"""
    if page_num <= 1:
        return redirect('/plans')
    
    plans = Plan.query.filter_by(private=False).order_by(Plan.id.desc()).limit(20).offset((page_num - 1) * 20).all()
    return render_template("/plans/index.html", plans=plans, page_num=page_num)

@app.route('/plans/new', methods=["GET", "POST"])
def create_plan():
    """Shows and handles form to create new garden plan."""

    if g.user:
        form = NewPlanForm()
        if form.validate_on_submit():
            title = form.title.data
            private = form.private.data
            owner_id = g.user.id

            NewPlan = Plan(title=title, private=private, owner_id=owner_id)
            db.session.add(NewPlan)
            db.session.commit()

            id = NewPlan.id
            # Incomplete
            flash('Plan created, add some plants to your plan!')
            return redirect("/search")
        return render_template("/plans/add.html", form=form)
        
    flash('Must be logged in to create a plan')
    return redirect("/login")

@app.route('/plans/<int:plan_id>/')
def show_plan(plan_id):
    """Shows list of plants within a given plan"""

    plan = Plan.query.get(plan_id)
    if plan.private is False or plan.owner_id == g.user.id:
        plant_roles = PlantRole.query.filter_by(plan_id = plan_id).all()
        plants=[]
        for plant_role in plant_roles:
            plant = requests.get(f"https://perenual.com/api/species/details/{plant_role.plant_id}?key={api_key}").json()
            plants.append(plant)            
        return render_template("/plans/show.html", plan=plan, plants=plants)
    flash("Not authorized to view this plan")
    return redirect("/plans")
    
# # Show plants contained in a given plan

# @app.route('/plans/<int:plan_id>/edit')
# # Page to allow user to remove plants from their plan

@app.route('/search', methods=["GET"])
def search():
    """Handles search from header search bar. If no search query, shows all plants"""

    search = request.args.get('q')

    if not search:
        plants = requests.get(
        f"https://perenual.com/api/species-list?key={api_key}"
    ).json()['data']
    else:
        plants = requests.get(
        f"https://perenual.com/api/species-list?key={api_key}&q={search}"
    ).json()['data']
        
    for plant in plants:
        if plant['id'] > 3000:
            plants.remove(plant)
            # This removes all plants not available in free version of API
    return render_template('search.html', plants=plants, api_key=api_key, page_num=1, search=search)
# # Advanced search option to search plants

@app.route('/search/page/<int:page_num>', methods=["GET", "POST"])
def next_page_search(page_num):
    """Shows subsequent pages of search results"""

    search = request.args.get('q')

    if not search:
        plants = requests.get(
        f"https://perenual.com/api/species-list?key={api_key}&page={page_num}"
    ).json()['data']
    else:
        plants = requests.get(
        f"https://perenual.com/api/species-list?key={api_key}&q={search}&page={page_num}"
    ).json()['data']
        
    for plant in plants:
        if plant['id'] > 3000:
            plants.remove(plant)
            # This removes all plants not available in free version of API

    return render_template('search.html', plants=plants, api_key=api_key, page_num=page_num, search=search)

@app.route('/plants/<int:plant_id>')
def show_plant(plant_id):
    """Shows details for a single plant"""

    plant = requests.get(
        f"https://perenual.com/api/species/details/{plant_id}?key={api_key}"
    ).json()

    return render_template('/plants/show.html', plant=plant)

@app.route('/plants/page/<int:page_num>')
def next_page_plants(page_num):
    """Shows all plants"""

    plants = requests.get(
        f"https://perenual.com/api/species-list?key={api_key}&page={page_num}"
    ).json()['data']

    return render_template('/plants/index.html', plants=plants, page_num=page_num)

@app.route('/addplant/<int:plant_id>', methods=["GET", "POST"])
def add_plant(plant_id):
    """Shows and handles form to add a plant to selected plan(s)"""
    if g.user:
        form = AddToPlanForm()
        form.plans.choices = [(p.id, p.title) for p in Plan.query.filter_by(owner_id = g.user.id).all()]
        # set_trace()
        if form.is_submitted():
            # plans = form.plans.data
            # for plan in plans:
            #     role = PlantRole(plant_id = plant_id, plan_id = plan.id)
            #     db.session.add(role)
            #     db.session.commit()
            # flash("TESTING")
            return redirect('/')
        return render_template('plants/add_to_plan.html', form=form, plant_id=plant_id)
    flash('Must be logged in to add to a plan')
    return redirect("/login")