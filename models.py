from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """Registered Users"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    zone = db.Column(db.Integer)
    country = db.Column(db.String)

    # Comment column wil lbe a list of all user comment IDs
    # comments = db.relationship('Comment')
    
    def __repr__(self):
        """Show info about User"""

        u = self
        return f"<User {u.id} {u.username} {u.email} {u.zone} {u.country}>"
    
    @classmethod
    def signup(cls, username, password, email):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            email=email
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """
        Find user with `username` and `password`.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    
class Plan(db.Model):
    """Users' Garden Plans"""

    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    private = db.Column(db.Boolean, default=False)

    owner = db.Relationship('User')

class PlantRole(db.Model):
    """Instances of plants in garden plans"""

    __tablename__ = 'plantroles'

    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), primary_key=True)
    plant_id = db.Column(db.Integer, primary_key=True)


class Comment(db.Model):
    """User comments on plant entries"""
    
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plant_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    user = db.relationship('User')



def connect_db(app):
    db.app = app
    db.init_app(app)