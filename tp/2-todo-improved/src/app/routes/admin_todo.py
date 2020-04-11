from app import app

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse

from app.data.taskDataAccess import TaskDataAccess
from app.data.userDataAccess import UserDataAccess
from app.forms.taskForm import TaskForm
from app.models.user import User
from app.routes.admin import is_administrator

import datetime

@app.route('/admin/list/<user_id>')
@login_required  
def admin_task_listing(user_id):
    if (not is_administrator()):
        return render_template('404.html.j2'), 404

    return render_template('todo/list.html.j2', tasks = TaskDataAccess.get_tasks(user_id), user = UserDataAccess.get_user(user_id), datetime = datetime)

@app.route('/admin/<user_id>/add', methods=['GET', 'POST'])
@login_required
def admin_task_add(user_id):
    if (not is_administrator()):
        return render_template('404.html.j2'), 404

    form = TaskForm()
    if form.validate_on_submit():
        TaskDataAccess.add_task(
            form.title.data,
            form.description.data,
            form.due_date.data,
            user_id
        )
        return redirect(url_for('admin_task_listing', user_id = user_id))
    else:
        return render_template('todo/add.html.j2', form = form, user = UserDataAccess.get_user(user_id))

@app.route('/admin/<user_id>/edit/<task_id>', methods=['GET', 'POST'])
@login_required
def admin_task_edit(user_id, task_id):
    if (not is_administrator()):
        return render_template('404.html.j2'), 404

    task = TaskDataAccess.get_task(task_id)
    
    form = TaskForm()

    if form.validate_on_submit():
        TaskDataAccess.update_task(
            form.id.data,
            form.title.data,
            form.description.data,
            form.due_date.data
        )
        return redirect(url_for('admin_task_listing', user_id = user_id))
    else:
        form.id.data = task.id
        form.title.data = task.title
        form.description.data = task.description
        form.due_date.data = task.due_date
        return render_template('todo/edit.html.j2', form = form, user = UserDataAccess.get_user(user_id))

@app.route('/admin/<user_id>/delete/<task_id>')
@login_required
def admin_task_delete(user_id, task_id):
    if (not is_administrator()):
        return render_template('404.html.j2'), 404
        
    task = TaskDataAccess.get_task(task_id)

    TaskDataAccess.delete_task(task_id)
    return redirect(url_for('admin_task_listing', user_id = user_id))

@app.route('/admin/<user_id>/status/<task_id>')
@login_required
def admin_task_status(user_id, task_id):
    if (not is_administrator()):
        return render_template('404.html.j2'), 404

    task = TaskDataAccess.get_task(task_id)

    TaskDataAccess.change_status(task_id)
    return redirect(url_for('admin_task_listing', user_id = user_id))