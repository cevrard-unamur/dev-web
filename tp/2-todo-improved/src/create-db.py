from app import db
from app.data.userDataAccess import UserDataAccess

import datetime
import logging

print('--- Database creation ---')

# re-create the database
print('The database is dropped and created')
db.drop_all()
db.create_all()

# create the default administrator accout
print('The SuperAdmin account is created')
UserDataAccess.add_user('admin', 'password', 'Super', 'Admin', datetime.datetime.now(), 'admin@evrard.io', 2)

print('The database has been created')