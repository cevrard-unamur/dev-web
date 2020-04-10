from app import app

from flask import render_template, redirect, url_for, request
from app.models.task import Task

# Création de deux tâches "par défaut" dans la ToDo liste.
tasks = [
    Task("Ma première tâche"),
    Task("Ma deuxième tâche")
]

# Point d'entré de l'application
@app.route('/')
def index():
    return render_template('index.html.j2', tasks = tasks)

# Insertion d'une nouvelle tâche dans la liste
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        _title = request.form['title']
        if(not(_title and _title.strip())): # Si le titre est vide, on retourne un message d'erreur
            return render_template('add.html.j2', error = "Le titre de la tâche ne peut être vide")
        else:
            tasks.append(Task(_title))
            return redirect(url_for('index'))
    else:
        return render_template('add.html.j2')

# Edition d'une tâche
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        _title = request.form['title']
        # On recherche la tâche qui a été éditée
        for task in tasks:
            if task.id == id:
                if(not(_title and _title.strip())): # Si le titre est vide, on retourne un message d'erreur
                    return render_template('edit.html.j2', task = task, error = "Le titre de la tâche ne peut être vide")
                else:
                    task.title = _title
        return redirect(url_for('index'))
    else:
        # On recherche la tâche qui à éditer
        for task in tasks:
            if task.id == id:
                return render_template('edit.html.j2', task = task)
        return render_template('404.html.j2'), 404 # Si celle-ci n'existe pas, on retourne l'utilisateur vers la page 404

# Suppression d'une †âche
@app.route('/delete/<id>')
def delete(id):
    # On recherche la tâche qui à supprimer
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            return redirect(url_for('index'))
    return render_template('404.html.j2'), 404  # Si celle-ci n'existe pas, on retourne l'utilisateur vers la page 404

# Changement du statut d'une tâche
@app.route('/status/<id>')
def status(id):
    # On recherche la tâche pour laquelle on veut changer le statut
    for task in tasks:
        if task.id == id:
            task.status = not task.status
            return redirect(url_for('index'))
    return render_template('404.html.j2'), 404  # Si celle-ci n'existe pas, on retourne l'utilisateur vers la page 404

# Page 404 retournée si l'URL entrée par l'utilisateur n'est pas connue
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html.j2'), 404