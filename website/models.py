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
    assignments = db.relationship('Assignment', cascade='all,delete', backref='User')
    course = db.relationship('Course', cascade='all,delete', backref='User')
    discussion = db.relationship('Discussion', cascade='all,delete', backref='User')
    notification = db.relationship('Notification', cascade='all,delete', backref='User')
    submission = db.relationship('Submission', cascade='all,delete', backref='User')
    enroll = db.relationship('Enroll', cascade='all,delete', backref='User')

    def __str__(self):
        return f"id : {self.id}, role is {self.role}, email is {self.email} "

class Assignment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000000000000000000000000000000))
    assign_date = db.Column(db.DateTime(timezone=True), default=func.now())
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    file = db.Column(db.String(150))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    submission = db.relationship('Submission', cascade='all,delete', backref='Assignment')

class Course(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    enroll_id = db.Column(db.Integer)
    material = db.relationship('Material', cascade='all,delete', backref='Course')
    notification = db.relationship('Notification', cascade='all,delete', backref='Course')
    assignment = db.relationship('Assignment', cascade='all,delete', backref='Course')
    enroll = db.relationship('Enroll', cascade='all,delete', backref='Course')

class Enroll(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Discussion(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())

class Material(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    description = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    file = db.Column(db.String(150))

class Notification(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(100))

class Submission(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    submitter = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    file = db.Column(db.String(150))
    mark = db.Column(db.Integer)
    comment = db.Column(db.String(100))
    def __str__(self):
        return f"id : {self.id}, submitter is {self.submitter}, description is {self.description} file is {self.file} "
