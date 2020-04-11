from app import app
from app import db
from app import mail

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse
from flask_mail import Message

from app.models.task import Task
from app.models.user import User
from app.forms.loginForm import LoginForm
from app.forms.registrationForm import RegistrationForm
from app.data.userDataAccess import UserDataAccess

import logging
import sys

@app.route('/login', methods=['get', 'post'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = UserDataAccess.get_by_username(form.username.data)
        if (user is None) or (not user.check_password(form.password.data)):
            flash('Connexion impossible. Veuillez vérifier votre nom d\'utilisateur et mot de passe', 'danger')
            return redirect(url_for('login'))
        if (user.is_locked):
            flash('Votre compte est bloqué. Veuillez contacter un administrateur', 'danger')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    else:
        return render_template('login/login.html.j2', form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = UserDataAccess.get_by_username(form.username.data)
        logging.error(user is None)
        if user is None:
            UserDataAccess.add_user(
                form.username.data, 
                form.password.data, 
                form.firstname.data,
                form.lastname.data,
                form.birthday.data,
                form.email.data)
            try:
                send_welcome_mail(
                    form.email.data,
                    form.username.data,
                    form.firstname.data,
                    form.lastname.data
                )
            except:
                e = sys.exc_info()[0]
                logging.error(e)
            flash('Votre compte a été créé, vous pouvez maintenant vous connecter', 'success')
            return redirect(url_for('login'))
        else :
            flash('Un compte existe déjà avec ce nom d\'utilisateur', 'danger')
            return render_template('login/registration.html.j2', form = form)
            
    return render_template('login/registration.html.j2', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def send_welcome_mail(to, username, firstname, lastname):
    msg = Message("Bienvenue sur ToDo !",
                sender="cedric@evrard.io",
                recipients=[to])
    msg.html = """
            <html>
                <head>
                </head> 
                <body>
                    <h1>
                        Bienvenue sur ToDo !
                    </h1>
                    Bonjour %s %s,
                    <br>
                    <br>
                    <br>
                    Votre nom d'utilisateur est <strong>%s</strong>.
                    <br>
                    Vous pouvez vous connecter au site via cette adresse : <a href="http://localhost:5000/login">http://localhost:5000/login</a> 
                </body>
            </html>
        """ % (firstname, lastname, username.lower())

    mail.send(msg)