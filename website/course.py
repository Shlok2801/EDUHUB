from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from . import db
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
import os
from .models import *
import json
course = Blueprint('course', __name__)

class UploadFileForm(FlaskForm):
    file = FileField('File', validators=[InputRequired()])
    submit = SubmitField('Upload')


@course.route('/course-s', methods=['GET', 'POST'])
@login_required
def view_student():
    if request.method=='POST':
        course_id = request.form.get('course_id')
        

        if course_id == "" :
            flash('Please enter course id!', category='error')
        elif Course.query.filter_by(enroll_id=course_id).first() :
            new_student = Enroll(course_id=course_id,user_id=current_user.id)
            db.session.add(new_student)
            db.session.commit()           
            flash('Enrolled successfully!', category='success')
    return render_template('home_student.html', user=current_user)
    #Remember to redirect to the course page when done

@course.route('/course-t', methods=['GET', 'POST'])
@login_required
def view_teacher():
    if current_user.role != "teacher":
        return render_template('home_student.html', user=current_user)
    if request.method=='POST':
        course_name = request.form.get('course_name')
        course_id = request.form.get('course_id')
        course_des = request.form.get('course_des')
        if course_id != '':
            id=Course.query.filter_by(enroll_id=course_id).first()

        if len(course_name) < 1:
            flash('Please enter an assignment!', category='error')
        elif len(course_des) < 10:
            flash('Please enter an assignment!', category='error')
        elif id:
            flash('Course id already exist', category='error')
        elif len(course_id) != 6:
            flash('Course id has to be 6 digits', category='error')            
        else:
            new_course = Course(name=course_name, description=course_des,creator=current_user.id,enroll_id= course_id)
            db.session.add(new_course)
            db.session.commit()
            flash('Course created successfully!', category='success')

    return render_template('teacher_manage_courses.html', user=current_user)

@course.route('/delete-assignment', methods=['POST'])
def delete_assignment():
    assignment = json.loads(request.data)
    assignmentId = assignment['assignmentId']
    assignment = Assignment.query.get(assignmentId)
    if assignment:
        if assignment.user_id == current_user.id:
            db.session.delete(assignment)
            db.session.commit()
            flash('Assignment deleted successfully!', category='success')
    return jsonify({})