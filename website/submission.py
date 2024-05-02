from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app, jsonify, send_from_directory
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from . import db
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
import os
from .models import *
import json
from distutils.log import debug 
from fileinput import filename 
from flask import *
from os import path
from sqlalchemy import desc,asc,update
from sqlalchemy.orm import sessionmaker

submission = Blueprint('submission', __name__)

ASSIGNMENTS = 'website/uploads/teacher/assignments'
ASSIGNMENTS2 = '/uploads/teacher/assignments'
SUBMISSIONS = 'website/uploads/submissions'
MATERIAL = 'website/uploads/teacher/material'

class UploadFileForm(FlaskForm):
    file = FileField('File', validators=[InputRequired()])
    submit = SubmitField('Upload')


@submission.route('/assignments-s/<id>', methods=['GET', 'POST'])
@login_required
def view_student(id):
    assignmentId = id
    assignment = Assignment.query.get(assignmentId)
    if not assignment:
        flash("Bad request")
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        submission=Submission.query.filter_by(assignment_id=assignmentId,submitter=current_user.id).first()
        if submission :
            return render_template('student-submit.html', user = current_user, assignment = assignment,submission=submission)
        file = request.files.get("file")
        desc = request.form.get('desc')
        if file:
            file.save(os.path.join(SUBMISSIONS, file.filename))
            new_submission = Submission(submitter=current_user.id, file=file.filename, description=desc, assignment_id=id)
        else:
            new_submission = Submission(submitter=current_user.id,description=desc, assignment_id=id)
        db.session.add(new_submission)
        db.session.commit()
        flash('Assignment submitted successfully!', category='success')
    submission = Submission.query.filter_by(assignment_id=assignmentId,submitter=current_user.id).first()
    #print(submission)
    return render_template('student-submit.html', user = current_user, assignment = assignment,submission=submission)
    
@submission.route('/downloadSub/<id>')
@login_required
def downloadSub(id):
    subId = id
    submission = Submission.query.get(subId)
    uploads_directory = os.path.join(current_app.root_path, 'uploads\\submissions')
    file_path = os.path.join(uploads_directory, submission.file)     
    return send_file(file_path,as_attachment=True)

@submission.route('/delete-sub', methods=['POST'])
def delete_sub():
    if current_user.role != "student":
        return redirect(url_for('views.home'))
    data = json.loads(request.data)
    subId = data['submissionId']
    submission = Submission.query.get(subId)
    if subId == '': 
        flash('No submission id', category='error')
        return redirect(url_for('views.home'))
    if submission.submitter == current_user.id :
        db.session.delete(submission)
        if submission.file:
            x = SUBMISSIONS.replace('website', "")
            y = x.replace("/", "\\")
            print(current_app.root_path)
            uploads = os.path.join(current_app.root_path, y)
            print(uploads)
            z = current_app.root_path+y+'\\'+submission.file
            z = z.replace("\\", "/")
            os.remove(z) 
            db.session.delete(submission)   
            db.session.commit()
        db.session.commit()
        flash('Submission deleted successfully!', category='success')
    return render_template('student_courses.html', user=current_user)


@submission.route('/delete-assignment', methods=['POST'])
def delete_assignment():
    if current_user.role != "teacher":
        return redirect(url_for('views.home'))
    assignment = json.loads(request.data)
    assignmentId = assignment['assignmentId']
    assignment = Assignment.query.get(assignmentId)
    if assignmentId == '': 
        flash('No assignment id', category='error')
        return redirect(url_for('views.home'))
    if assignment.creator == current_user.id :
        db.session.delete(assignment)
        if assignment.file:
            x = ASSIGNMENTS.replace('website', "")
            y = x.replace("/", "\\")
            print(current_app.root_path)
            uploads = os.path.join(current_app.root_path, y)
            print(uploads)
            z = current_app.root_path+y+'\\'+assignment.file
            z = z.replace("\\", "/")
            os.remove(z) 
            db.session.delete(assignment)   
            db.session.commit()
        db.session.commit()
        flash('Assignment deleted successfully!', category='success')
    return render_template('teacher-create.html', user=current_user)

@submission.route('/downloadAssignment/<id>')
@login_required
def downloadAssignment(id):
    assignmentId = id
    assignment = Assignment.query.get(assignmentId)
    uploads_directory = os.path.join(current_app.root_path, 'uploads\\teacher\\assignments')
    file_path = os.path.join(uploads_directory, assignment.file)     
    return send_file(file_path,as_attachment=True)

@submission.route('/Assignments/<id>',methods=["GET",'POST'])
@login_required
def view_t(id):
    courseId = id
    course = Course.query.get(courseId)
    if course is None or current_user.id != course.creator:
        flash("Bad request")
        return redirect(url_for('views.home'))
    assignments = Assignment.query.filter_by(course_id=courseId).all()
    if request.method == 'POST':
        assignment_data = request.form.get('assignment')
        file = request.files["file"]
        if not assignment_data:
            return flash('Enter an assignment', category='error')
        else:
            if file:
                file.save(os.path.join(ASSIGNMENTS, file.filename))
                new_assignment = Assignment(data=assignment_data, creator=current_user.id, file=file.filename, course_id=courseId)
            else:
                new_assignment = Assignment(data=assignment_data, creator=current_user.id ,course_id=courseId )
        
            db.session.add(new_assignment)
            db.session.commit()
        
            flash('Assignment created successfully!', category='success')
            return render_template('teacher_manage_courses.html', user=current_user)
    else:
        return render_template('teacher-create.html', user=current_user, assignments=assignments)
        

@submission.route('/Material/<id>', methods=["GET", 'POST'])
@login_required
def material(id):
    courseId = id
    course = Course.query.get(courseId)
    if course is None or current_user.id != course.creator:
        flash("Bad request")
        return redirect(url_for('views.home'))
    
    material = Material.query.filter_by(course_id=courseId).all()
    
    if request.method == 'POST':
        description = request.form.get('description')
        file = request.files.get("file")
        if not description:
            flash('Enter a description', category='error')
        else:
            if file:
                file.save(os.path.join(MATERIAL, secure_filename(file.filename)))
                new_material = Material(description=description, file=file.filename, course_id=courseId, creator=current_user.id)
            else:
                new_material = Material(description=description, course_id=courseId, creator=current_user.id)
        
            db.session.add(new_material)
            db.session.commit()
        
            flash('Material added successfully!', category='success')
            return render_template('teacher_manage_courses.html', user=current_user)
    return render_template('t_manage_material.html', user=current_user, material=material)

    
@submission.route('/delete-material', methods=['POST'])
def delete_material():
    if current_user.role != "teacher":
        return redirect(url_for('views.home'))
    material = json.loads(request.data)
    materialId = material['materialId']
    material = Material.query.get(materialId)
    if materialId == '': 
        flash('No material id', category='error')
        return redirect(url_for('views.home'))
    x = MATERIAL.replace('website', "")
    y = x.replace("/", "\\")
    print(current_app.root_path)
    uploads = os.path.join(current_app.root_path, y)
    print(uploads)
    z = current_app.root_path+y+'\\'+material.file
    z = z.replace("\\", "/")
    os.remove(z) 
    db.session.delete(material)   
    db.session.commit()
    flash('Material deleted successfully!', category='success')
    return render_template('t_manage_material.html', user=current_user)

@submission.route('/downloadMaterial/<id>')
@login_required
def downloadMaterial(id):
    materialId = id
    material = Material.query.get(materialId)
    uploads_directory = os.path.join(current_app.root_path, 'uploads\\teacher\\material')
    file_path = os.path.join(uploads_directory, material.file)     
    return send_file(file_path,as_attachment=True)

@submission.route('/Submissions/<id>', methods=["GET", 'POST'])
@login_required
def viewSubs(id):
    if request.method=="POST":
        body = json.loads(request.data)
        comment = body['comment']
        mark = body['mark']
        subId = body["subId"]
        print(comment,mark,subId)
        if mark>10:
            flash("The mark can't be more than 10", category="error")
            return redirect(url_for('views.home'))
        if subId == "":
            flash("bad request", category="error")
            return redirect(url_for('views.home'))
        
        sub = db.session.query(Submission).filter_by(id=subId).first()
        sub.mark= mark
        sub.comment=comment
        db.session.commit()

    assignmentId = id
    assignment = Assignment.query.get(assignmentId)
    #submissions = Submission.query.filter_by(assignmentId).all()
    if assignment is None or current_user.id != assignment.creator:
        flash("Bad request")
        return redirect(url_for('views.home'))
    submissions = db.session.query(User, Submission).filter(Submission.submitter == User.id).filter(Submission.assignment_id==assignmentId).order_by(asc(Submission.timestamp)).all()
    return render_template('view_submissions.html', user=current_user, submissions=submissions)


