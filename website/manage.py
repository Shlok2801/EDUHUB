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
manage = Blueprint('manage', __name__)

class UploadFileForm(FlaskForm):
    file = FileField('File', validators=[InputRequired()])
    submit = SubmitField('Upload')



@manage.route('/manage-t', methods=['GET', 'POST'])
@login_required
def view_student():
    return render_template('teacher_manage_courses.html', user=current_user)

"""@manage.route('/', methods=['GET', 'POST'])
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
    #Remember to redirect to the course page when done"""

@manage.route('/delete-course', methods=['GET', 'POST'])
@login_required
def deleteCourse():
    if current_user.role != "teacher":
        return render_template('home_student.html', user=current_user)
    if request.method=='POST':
        courseId = json.loads(request.data)
        courseId = courseId['courseId']
        if courseId == '': flash('Course id has to be 6 digits', category='error')
        course=Course.query.get(courseId)
        if course.creator == current_user.id : 
            db.session.delete(course)
            db.session.commit()
            flash('Course deleted successfully!', category='success')

    return jsonify({})

