from alfanso import db
from flask_login import UserMixin


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    registration_no = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    rull = db.Column(db.Integer, nullable=False, unique=True)
    roll_in_school = db.Column(db.String(60), default='student')




class Student_login(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    registration_no = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)



class Principle(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    status = db.Column(db.String(60), default='present')
    roll_in_school = db.Column(db.String(60), default='principle')
