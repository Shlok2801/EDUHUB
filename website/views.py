from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    role = current_user.role
    if role == 'student':
        return render_template('home_student.html', user=current_user)
    else:
        return render_template('home_teacher.html', user=current_user)