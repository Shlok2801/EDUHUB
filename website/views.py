from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app
from flask_login import login_required, current_user
from . import db
import json
from werkzeug.utils import secure_filename
import os


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    role = current_user.role
    print(role)
    if role == 'student':
        return redirect('/course-s')
        #return render_template('home_student.html', user=current_user)
    else:
        return render_template('home_teacher.html', user=current_user)

