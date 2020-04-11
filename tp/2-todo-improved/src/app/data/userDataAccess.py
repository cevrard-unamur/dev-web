from app import db

from app.models.user import User

import logging

class UserDataAccess():
    def add_user(username, password, firstname, lastname, birthday, email, account_level = 0):
        user = User(username.lower(), firstname, lastname, birthday, email, account_level)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

    def get_users():
        return User.query.all()

    def get_user(user_id):
        return User.query.filter_by(id = user_id).first()

    def get_by_username(username):
        return User.query.filter_by(username = username.lower()).first()

    def change_status(user_id):
        user = User.query.filter_by(id = user_id).first()

        if user.account_level == 0:
            user.account_level = 1
        else:
            user.account_level = 0
        
        db.session.commit()

    def change_lock(user_id):
        user = User.query.filter_by(id = user_id).first()
        user.is_locked = not user.is_locked        
        db.session.commit()

    def delete(user_id):
        user = User.query.filter_by(id = user_id).first()
        db.session.delete(user)
        db.session.commit()