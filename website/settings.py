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
settings = Blueprint('settings', __name__)

class UploadFileForm(FlaskForm):
    file = FileField('File', validators=[InputRequired()])
    submit = SubmitField('Upload')


@settings.route('/settings', methods=['GET', 'POST'])
@login_required
def view():
    if request.method=='GET':
        return render_template('user_settings.html', user=current_user)
    if request.method=='POST':
        if (current_user.id) :
            toDelete=User.query.get(current_user.id)
            db.session.delete(toDelete)
            db.session.commit()
            flash('User deleted successfully!', category='success')
    return redirect(url_for('views.home'))

