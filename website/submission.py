from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app, send_file
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
import os
import json
from . import db
from .models import *
from sqlalchemy import asc
import uuid

submission = Blueprint('submission', __name__)

ASSIGNMENTS = 'website/uploads/teacher/assignments'
SUBMISSIONS = 'website/uploads/submissions'
MATERIAL = 'website/uploads/teacher/material'

class UploadFileForm(FlaskForm):
    file = FileField('File', validators=[InputRequired()])
    submit = SubmitField('Upload')

def generate_unique_filename(filename):
    unique_id = str(uuid.uuid4())
    file_name, file_extension = os.path.splitext(filename)
    return secure_filename(f"{file_name}_{unique_id}{file_extension}")

@submission.route('/assignments-s/<id>', methods=['GET', 'POST'])
@login_required
def view_student(id):
    assignmentId = id
    assignment = Assignment.query.get(assignmentId)
    if not assignment:
        flash("Bad request")
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        submission = Submission.query.filter_by(assignment_id=assignmentId, submitter=current_user.id).first()
        if submission:
            return render_template('student-submit.html', user=current_user, assignment=assignment, submission=submission)
        file = request.files.get("file")
        desc = request.form.get('desc')
        if file:
            filename = generate_unique_filename(file.filename)
            file.save(os.path.join(SUBMISSIONS, filename))
            new_submission = Submission(submitter=current_user.id, file=filename, description=desc, assignment_id=id)
        else:
            new_submission = Submission(submitter=current_user.id, description=desc, assignment_id=id)
        db.session.add(new_submission)
        db.session.commit()
        flash('Assignment submitted successfully!', category='success')
    submission = Submission.query.filter_by(assignment_id=assignmentId, submitter=current_user.id).first()
    return render_template('student-submit.html', user=current_user, assignment=assignment, submission=submission)

@submission.route('/downloadSub/<id>')
@login_required
def downloadSub(id):
    subId = id
    submission = Submission.query.get(subId)
    uploads_directory = os.path.join(current_app.root_path, 'uploads/submissions')
    file_path = os.path.join(uploads_directory, submission.file)     
    return send_file(file_path,as_attachment=True)

@submission.route('/delete-sub', methods=['POST'])
@login_required
def delete_sub():
    if current_user.role != "student":
        return redirect(url_for('views.home'))
    data = json.loads(request.data)
    subId = data['submissionId']
    submission = Submission.query.get(subId)
    if not submission:
        flash('No submission found', category='error')
        return redirect(url_for('views.home'))

    if submission.file:
        file_path = os.path.join(SUBMISSIONS, submission.file)
        if os.path.exists(file_path):
            os.remove(file_path)
            
    db.session.delete(submission)
    db.session.commit()
    
    flash('Submission deleted successfully!', category='success')
    return render_template('student_courses.html', user=current_user)

@submission.route('/delete-assignment', methods=['POST'])
@login_required
def delete_assignment():
    if current_user.role != "teacher":
        return redirect(url_for('views.home'))
    data = json.loads(request.data)
    assignmentId = data['assignmentId']
    assignment = Assignment.query.get(assignmentId)
    if not assignment:
        flash('No assignment found', category='error')
        return redirect(url_for('views.home'))

    if assignment.file:
        file_path = os.path.join(ASSIGNMENTS, assignment.file)
        if os.path.exists(file_path):
            os.remove(file_path)
            
    db.session.delete(assignment)
    db.session.commit()
    
    flash('Assignment deleted successfully!', category='success')
    return render_template('teacher-create.html', user=current_user)

@submission.route('/downloadAssignment/<id>')
@login_required
def downloadAssignment(id):
    assignmentId = id
    assignment = Assignment.query.get(assignmentId)
    uploads_directory = os.path.join(current_app.root_path, 'uploads/teacher/assignments')
    file_path = os.path.join(uploads_directory, assignment.file)     
    return send_file(file_path,as_attachment=True)

@submission.route('/Assignments/<id>', methods=["GET", 'POST'])
@login_required
def view_t(id):
    courseId = id
    course = Course.query.get(courseId)
    if not course or current_user.id != course.creator:
        flash("Bad request")
        return redirect(url_for('views.home'))
    assignments = Assignment.query.filter_by(course_id=courseId).all()
    if request.method == 'POST':
        assignment_data = request.form.get('assignment')
        file = request.files.get("file")
        if not assignment_data:
            flash('Enter an assignment', category='error')
        else:
            if file:
                filename = generate_unique_filename(file.filename)
                file.save(os.path.join(ASSIGNMENTS, filename))
                new_assignment = Assignment(data=assignment_data, creator=current_user.id, file=filename, course_id=courseId)
            else:
                new_assignment = Assignment(data=assignment_data, creator=current_user.id, course_id=courseId)
            db.session.add(new_assignment)
            db.session.commit()
            flash('Assignment created successfully!', category='success')
            return render_template('teacher_manage_courses.html', user=current_user)
    return render_template('teacher-create.html', user=current_user, assignments=assignments)

@submission.route('/Material/<id>', methods=["GET", 'POST'])
@login_required
def material(id):
    courseId = id
    course = Course.query.get(courseId)
    if not course or current_user.id != course.creator:
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
                filename = generate_unique_filename(file.filename)
                file.save(os.path.join(MATERIAL, filename))
                new_material = Material(description=description, file=filename, course_id=courseId, creator=current_user.id)
            else:
                new_material = Material(description=description, course_id=courseId, creator=current_user.id)
            db.session.add(new_material)
            db.session.commit()
            flash('Material added successfully!', category='success')
            return render_template('teacher_manage_courses.html', user=current_user)
    return render_template('t_manage_material.html', user=current_user, material=material)

@submission.route('/delete-material', methods=['POST'])
@login_required
def delete_material():
    if current_user.role != "teacher":
        return redirect(url_for('views.home'))
    data = json.loads(request.data)
    materialId = data['materialId']
    material = Material.query.get(materialId)
    if not material:
        flash('No material found', category='error')
        return redirect(url_for('views.home'))

    if material.file:
        file_path = os.path.join(MATERIAL, material.file)
        if os.path.exists(file_path):
            os.remove(file_path)
            
    db.session.delete(material)
    db.session.commit()
    
    flash('Material deleted successfully!', category='success')
    return render_template('t_manage_material.html', user=current_user)

@submission.route('/downloadMaterial/<id>')
@login_required
def downloadMaterial(id):
    materialId = id
    material = Material.query.get(materialId)
    uploads_directory = os.path.join(current_app.root_path, 'uploads/teacher/material')
    file_path = os.path.join(uploads_directory, material.file)     
    return send_file(file_path,as_attachment=True)

@submission.route('/Submissions/<id>', methods=["GET", 'POST'])
@login_required
def viewSubs(id):
    if request.method == "POST":
        body = json.loads(request.data)
        comment = body['comment']
        mark = body['mark']
        subId = body["subId"]
        if mark > 10:
            flash("The mark can't be more than 10", category="error")
            return redirect(url_for('views.home'))
        if subId == "":
            flash("Bad request", category="error")
            return redirect(url_for('views.home'))
        sub = Submission.query.get(subId)
        if sub:
            sub.mark = mark
            sub.comment = comment
            db.session.commit()
    assignmentId = id
    assignment = Assignment.query.get(assignmentId)
    if not assignment or current_user.id != assignment.creator:
        flash("Bad request")
        return redirect(url_for('views.home'))
    submissions = db.session.query(User, Submission).filter(Submission.submitter == User.id).filter(Submission.assignment_id == assignmentId).order_by(asc(Submission.timestamp)).all()
    return render_template('view_submissions.html', user=current_user, submissions=submissions)
