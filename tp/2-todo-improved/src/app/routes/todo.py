from app import app

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse

from app.data.taskDataAccess import TaskDataAccess
from app.forms.taskForm import TaskForm
from app.models.task import Task
from app.models.user import User
from app.routes.admin import is_administrator

import logging
import datetime

# Point d'entré de l'application
@app.route('/')
@login_required
def index():
    return redirect(url_for('listing'))

@app.route('/list')
@login_required
def listing():
    return render_template('todo/list.html.j2', tasks = TaskDataAccess.get_tasks(current_user.get_id()), datetime = datetime)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = TaskForm()
    if form.validate_on_submit():
        TaskDataAccess.add_task(
            form.title.data,
            form.description.data,
            form.due_date.data,
            current_user.get_id()
        )
        return redirect(url_for('listing'))
    else:
        return render_template('todo/add.html.j2', form = form)

@app.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    task = TaskDataAccess.get_task(id)

    if canAccessToTask(task):
        form = TaskForm()

        if form.validate_on_submit():
            TaskDataAccess.update_task(
                form.id.data,
                form.title.data,
                form.description.data,
                form.due_date.data
            )
            return redirect(url_for('listing'))
        else:
            form.id.data = task.id
            form.title.data = task.title
            form.description.data = task.description
            form.due_date.data = task.due_date
            return render_template('todo/edit.html.j2', form = form)   
    else:
        return render_template('404.html.j2'), 404

@app.route('/delete/<id>')
@login_required
def delete(id):
    task = TaskDataAccess.get_task(id)

    if canAccessToTask(task):
        TaskDataAccess.delete_task(id)
        return redirect(url_for('listing'))
    else:
        return render_template('404.html.j2'), 404

@app.route('/status/<id>')
@login_required
def status(id):
    task = TaskDataAccess.get_task(id)

    if canAccessToTask(task):
        TaskDataAccess.change_status(id)
        return redirect(url_for('listing'))

    return render_template('404.html.j2'), 404

def canAccessToTask(task):
    return task.user_id == int(current_user.get_id()) or is_administrator()

