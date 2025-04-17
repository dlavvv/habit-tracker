from app import db
from flask_login import UserMixin

class Users(UserMixin, db.Model): # inherits is_authenticated from UserMixin
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

class Habits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completion_time = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)

class Lists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completion_time = db.Column(db.DateTime, nullable=True)
    list_id = db.Column(db.Integer, db.ForeignKey(Lists.id), nullable=False)
    list = db.relationship(Lists, backref='tasks') # to be able to access all tasks in a list without extra code
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)

