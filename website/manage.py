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
def view():
    if  current_user.role == "teacher" :
        return render_template('teacher_manage_courses.html', user=current_user)
    else :
        return redirect(url_for('views.home'))

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
        return redirect(url_for('views.home'))
    if request.method=='POST':
        courseId = json.loads(request.data)
        courseId = courseId['courseId']
        if courseId == '': 
            flash('No course id', category='error')
            return redirect(url_for('views.home'))
        course=Course.query.get(courseId)
        if course.creator == current_user.id : 
            db.session.delete(course)
            db.session.commit()
            flash('Course deleted successfully!', category='success')

    return jsonify({})

@manage.route('/enrolled-students', methods=['GET', 'POST'])
@login_required
def enrolledStudents():    
        courseId=request.args.get("id")
        if courseId == '': 
            flash('Wrong request', category='error')
            #return redirect(url_for('views.home'))
        course=Course.query.get(courseId)
        enrolled=Enroll.query.filter_by(course_id=courseId)
        students=[]
        for single in enrolled :
            x= User.query.filter_by(id=single.user_id).first()
            students.append(x)
            print(str(x))
            print(students)
        if not students :
            flash('There are no enrolled students to this course', category='info')
            return render_template('teacher_manage_courses.html', user=current_user)

        return render_template('enrolled_students.html', user=current_user,course=course,students=students)
    
@manage.route('/unenroll-student', methods=['POST'])
@login_required
def unenrollStudent():
    if current_user.role != "teacher":
        return redirect(url_for('views.home'))
    if request.method=='POST':
        data = json.loads(request.data)
        courseId = data['courseId']
        userId = data["userId"]
    if courseId == '' or userId == '':
        flash('Bad request ', category='error')
        return redirect(url_for('views.home'))
    course=Course.query.get(courseId)
    if not course:
        flash('Bad request, course not found ', category='error')
        return redirect(url_for('views.home'))
    enroll=Enroll.query.filter_by(course_id=courseId,user_id=userId).first()
    if not enroll:
        flash('Bad request, this student is not enrolled to this course ', category='error')
        return redirect(url_for('views.home'))
    if course.creator == current_user.id :
        db.session.delete(enroll)
        db.session.commit()
        flash('Student unenrolled succesfully', category='success')
    else:
        flash('Bad request, you do not have the permission ot perform this action ! ', category='error')
        return redirect(url_for('views.home'))

    return jsonify({})

@manage.route('/unenroll-me', methods=['POST'])
@login_required
def unenrollme():
    if current_user.role != "student":
        return redirect(url_for('views.home'))
    if request.method=='POST':
        data = json.loads(request.data)
        courseId = data['courseId']
        userId = data["userId"]
        print(courseId,userId,current_user.id)
    if courseId == '' or userId == '':
        flash('Bad request ', category='error')
        return redirect(url_for('views.home'))
    course=Course.query.get(courseId)
    if not course:
        flash('Bad request, course not found ', category='error')
        return redirect(url_for('views.home'))
    enroll=Enroll.query.filter_by(course_id=courseId,user_id=userId).first()
    if enroll.user_id != current_user.id:
        flash('Bad request ', category='error')
        return redirect(url_for('views.home'))
    if not enroll:
        flash('Bad request, this student is not enrolled to this course ', category='error')
        return redirect(url_for('views.home'))
    print("this is the current user id",current_user.id)
    db.session.delete(enroll)
    db.session.commit()
    flash('Student unenrolled succesfully', category='success')


    return jsonify({})
