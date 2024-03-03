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
    country = db.Column(db.Text)

    comments = db.relationship('Comment')

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
    
class Plan(db.Model):
    """Users' Garden Plans"""

    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

# class PlantRole(db.Model):
#     """Instances of plants in garden plans"""

#     __tablename__ = 'plantroles'

#     id = db.Column(db.Integer, primary_key=True)
#     # plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'))
#     plant_id = db.Column(db.Integer)


# class Comment(db.Model):
#     """User comments on plant entries"""
    
#     __tablename__ = 'comments'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'), primary_key=True)
#     comment = db.Column(db.Text, nullable=False)

#     user = db.relationship('User')



def connect_db(app):
    db.app = app
    db.init_app(app)