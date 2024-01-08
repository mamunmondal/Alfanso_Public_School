from alfanso import db
from flask_login import UserMixin,current_user
from datetime import datetime
from sqlalchemy.orm import relationship



class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key =True)
    type = db.Column(db.String(30))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'user'
        }
    

class PersonalInfo():
    name = db.Column(db.String(50), nullable=False)


class Student(User,PersonalInfo):
    __tablename__ = 'student'
    __mapper_args__ = {'polymorphic_identity': 'student'}

    id = db.Column(db.Integer,db.ForeignKey('user.id'), primary_key =True)
    username = db.Column(db.String(50), nullable=False)
    class_name = db.Column(db.Integer, nullable=False)
    registration_no = db.Column(db.String(20), nullable=False, unique=True)
    rull = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(20), default=lambda self: self.username + "@aps.com")
    posts = relationship('Post', backref='student', lazy=True)



class Principle(User,PersonalInfo):
    __tablename__ = 'principle'
    __mapper_args__ = {'polymorphic_identity': 'principle'} 
    
    id = db.Column(db.Integer,db.ForeignKey('user.id'), primary_key =True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    status = db.Column(db.String(60), default='present')
    posts = relationship('Post', backref='principle', lazy=True)

class Post(db.Model):
    __tablename__ = 'post'
    __mapper_args__ = {'polymorphic_identity': 'post'} 

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(20), nullable=False, default=lambda: current_user.name if current_user.is_authenticated else None)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)

    # Define foreign keys for the relationships
    student_id = db.Column(db.Integer, db.ForeignKey('student.id' , name="fk_stuent_post"))
    principle_id = db.Column(db.Integer, db.ForeignKey('principle.id' , name="fk_stuent_post"))


