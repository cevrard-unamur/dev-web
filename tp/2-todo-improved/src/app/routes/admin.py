from app import app

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse

from app.data.taskDataAccess import TaskDataAccess
from app.data.userDataAccess import UserDataAccess
from app.forms.taskForm import TaskForm
from app.models.user import User

@app.route('/admin')
@login_required
def admin():
    if (not is_administrator()):
        return render_template('404.html.j2'), 404

    return render_template('admin/admin.html.j2', users = UserDataAccess.get_users())

@app.route('/admin/status/<user_id>')
@login_required
def admin_status(user_id):
    if (not is_administrator()):
        return render_template('404.html.j2'), 404

    UserDataAccess.change_status(user_id)
    return redirect(url_for('admin'))

@app.route('/admin/lock/<user_id>')
@login_required
def admin_lock(user_id):
    if (not is_administrator()):
        return render_template('404.html.j2'), 404

    UserDataAccess.change_lock(user_id)
    return redirect(url_for('admin'))

@app.route('/admin/delete/<user_id>')
@login_required
def admin_delete(user_id):
    if (not is_administrator()):
        return render_template('404.html.j2'), 404

    UserDataAccess.delete(user_id)
    return redirect(url_for('admin'))     

def is_administrator():
    return current_user.account_level == 1 or current_user.account_level == 2
