from app import db
from flask_sqlalchemy import SQLAlchemy

# Modèle représentant une tâche.
# Celle-ci est composée d'un identifiant (généré automatiquement), d'un titre et d'un status
class Task(db.Model):

    __tablename__ = 'tasks'

    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(50), nullable=False)
    description     = db.Column(db.String(300), nullable=True)
    due_date        = db.Column(db.DateTime(), nullable=True)
    status          = db.Column(db.Boolean(), nullable=False, default=False)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id
        self.due_date = None
        self.description = ''

    def set_description(self, description):
        self.description = description
    
    def set_due_date(self, due_date):
        self.due_date = due_date

    def change_status(self):
        self.status = not self.status