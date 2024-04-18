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
from sqlalchemy import desc,asc

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
            return redirect(url_for('views.home'))
        course=Course.query.filter_by(enroll_id=course_id).first()
        if course:
            isEnrolled = Enroll.query.filter_by(course_id=course.id,user_id=current_user.id).first()
            if isEnrolled:
                flash('You are already enrolled into this course !', category='error')
                return redirect(url_for('views.home'))
            new_student = Enroll(course_id=course.id,user_id=current_user.id)
            db.session.add(new_student)
            db.session.commit()           
            flash('Enrolled successfully!', category='success')
        else:
            flash('Course not found', category='error')
    return render_template('home_student.html', user=current_user)
    #Remember to redirect to the course page when done

@course.route('/student-courses', methods=['GET', 'POST'])
@login_required
def viewmycourses():
    enrolled=Enroll.query.filter_by(user_id=current_user.id).all()
    courses = []
    for x in enrolled:
        courses.append(Course.query.get(x.course_id))
    return render_template('student_courses.html', user=current_user, courses=courses)
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
            flash('Please enter a name!', category='error')
            return render_template('teacher_create_course.html', user=current_user)
        elif len(course_des) < 10:
            flash('Please enter a description for your course!', category='error')
            return render_template('teacher_create_course.html', user=current_user)
        elif id:
            flash('Course id already exist', category='error')
            return render_template('teacher_create_course.html', user=current_user)
        elif len(course_id) != 6:
            flash('Course id has to be 6 digits', category='error')
            return render_template('teacher_create_course.html', user=current_user)            
        else:
            new_course = Course(name=course_name, description=course_des,creator=current_user.id,enroll_id= course_id)
            db.session.add(new_course)
            db.session.commit()
            flash('Course created successfully!', category='success')
        return render_template('teacher_manage_courses.html', user=current_user)
    return render_template('teacher_create_course.html', user=current_user)

@course.route('/course/<id>',methods=['GET', 'POST'])
@login_required
def viewCourseById(id):
    if request.method=="POST":
        courseId=id
        body = json.loads(request.data)
        message = body['message']
        print(message)
        if courseId == "":
            flash("bad request", category="error")
            return redirect(url_for('views.home'))
        new_message = Discussion(message=message,course_id=courseId,user_id=current_user.id)
        db.session.add(new_message)
        db.session.commit()
        #print("COMMITTED")
    courseId = id
    course = Course.query.get(courseId)
    if not course:
        flash('Invalid course id!', category='error')
        return redirect(url_for('views.home'))
    assignments = Assignment.query.filter_by(course_id=courseId).all()
    discussion = db.session.query(User, Discussion).filter(Discussion.user_id == User.id).filter(Discussion.course_id==courseId).order_by(asc(Discussion.timestamp)).all()
    material = Material.query.filter_by(course_id=courseId).all()
    #discussion is an obj like [(<User 2>, <Discussion 2>), (<User 2>, <Discussion 1>)]
    return render_template("course.html", user=current_user, course=course,assignments=assignments, discussion=discussion,material=material)