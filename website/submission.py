from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app, jsonify, send_from_directory
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from . import db
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
import os
from .models import Assignment, User
import json
from distutils.log import debug 
from fileinput import filename 
from flask import *
from os import path

submission = Blueprint('submission', __name__)

ASSIGNMENTS = 'website/uploads/teacher/assignments'

class UploadFileForm(FlaskForm):
    file = FileField('File', validators=[InputRequired()])
    submit = SubmitField('Upload')


@submission.route('/assignments-s', methods=['GET', 'POST'])
@login_required
def view_student():
    return render_template('student-submit.html', user=current_user)

@submission.route('/assignments-t', methods=['GET', 'POST'])
@login_required
def view_teacher():
    if request.method == 'POST':
        assignment_data = request.form.get('assignment')
        file = request.files["file"]
        if not assignment_data:
            flash('Enter an assignment', category='error')
        else:
            if file:
                file.save(os.path.join(ASSIGNMENTS, file.filename))
                new_assignment = Assignment(data=assignment_data, creator=current_user.id, file=file.filename)
            else:
                new_assignment = Assignment(data=assignment_data, creator=current_user.id)
        
            db.session.add(new_assignment)
            db.session.commit()
        
        flash('Assignment created successfully!', category='success')
        

    return render_template('teacher-create.html', user=current_user)

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
    if assignment.file:
            os.remove(assignment.file)
    if assignment.creator == current_user.id : 
        db.session.delete(assignment)
        db.session.commit()
        flash('Assignment deleted successfully!', category='success')
    return jsonify({})

@submission.route('/download', methods=["POST"])
@login_required
def download():
    if request.method == 'POST':
        assignment = json.loads(request.data)
        assignmentId = assignment['id']
        assignment = Assignment.query.get(assignmentId)
        if assignment.file:
            x=ASSIGNMENTS.replace("website","")
            x.replace("/","\\")
            print(x)

            return send_file(x,assignment.file)
        
        return jsonify({})

