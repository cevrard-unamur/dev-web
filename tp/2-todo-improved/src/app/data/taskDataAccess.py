from app import db

from app.models.task import Task

import logging

class TaskDataAccess():
    def add_task(title, description, due_date, user_id):
        task = Task(title, user_id)
        if(description and description.strip()):
            task.set_description(description)
        if(due_date):
            task.set_due_date(due_date)
        db.session.add(task)
        db.session.commit()

    def update_task(task_id, title, description, due_date):
        task = Task.query.filter_by(id = task_id).first()
        task.title = title
        task.description = description
        task.due_date = due_date
        db.session.commit()

    def get_tasks(user_id):
        return Task.query.filter_by(user_id = user_id).all()
    
    def get_task(task_id):
        return Task.query.filter_by(id = task_id).first()

    def change_status(task_id):
        task = Task.query.filter_by(id = task_id).first()
        task.change_status()
        db.session.commit()

    def delete_task(task_id):
        task = Task.query.filter_by(id = task_id).first()
        db.session.delete(task)
        db.session.commit()