from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(150), unique=True) 
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    role = db.Column(db.String(150))
    assignments = db.relationship('Assignment')
    course = db.relationship('Course')
    discussion = db.relationship('Discussion')
    notification = db.relationship('Notification')
    submission = db.relationship('Submission')
    enroll = db.relationship('Enroll')
    
class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000000000000000000000000000000))
    assign_date = db.Column(db.DateTime(timezone=True), default=func.now())
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    file = db.Column(db.String(150))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    enroll_id = db.Column(db.Integer) 
    material = db.relationship('Material')
    notification = db.relationship('Notification')
    assignment = db.relationship('Assignment')
    enroll = db.relationship('Enroll')

class Enroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    description = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    file = db.Column(db.String(150))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(100))

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    submitter = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    file = db.Column(db.String(150))

