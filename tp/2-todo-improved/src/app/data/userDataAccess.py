from app import db

from app.models.user import User

import logging

class UserDataAccess():
    def addUser(username, password, firstname, lastname, birthday, email, accountLevel = 0):
        user = User(username, firstname, lastname, birthday, email, accountLevel)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()