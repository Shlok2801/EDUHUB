from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from . import db
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
import os
from .models import Assignment, User
import json
submission = Blueprint('submission', __name__)

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
    if request.method=='POST':
        assignment = request.form.get('assignment')
        if len(assignment) < 1:
            flash('Please enter an assignment!', category='error')
        else:
            new_assignment = Assignment(data=assignment, creator=current_user.id)
            db.session.add(new_assignment)
            db.session.commit()
            flash('Assignment created successfully!', category='success')

    return render_template('teacher-create.html', user=current_user)

@submission.route('/delete-assignment', methods=['POST'])
def delete_assignment():
    assignment = json.loads(request.data)
    assignmentId = assignment['assignmentId']
    assignment = Assignment.query.get(assignmentId)
    if assignment:
        if assignment.creator == current_user.id:
            db.session.delete(assignment)
            db.session.commit()
            flash('Assignment deleted successfully!', category='success')
    return jsonify({})