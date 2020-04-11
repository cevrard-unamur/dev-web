from app import app

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse

from app.models.user import User

@app.route('/admin')
@login_required
def admin():
    return render_template('admin/admin.html.j2')