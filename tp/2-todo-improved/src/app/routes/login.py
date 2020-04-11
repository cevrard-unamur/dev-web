from app import app
from app import db

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse

from app.models.task import Task
from app.models.user import User
from app.forms.loginForm import LoginForm
from app.forms.registrationForm import RegistrationForm
from app.data.userDataAccess import UserDataAccess

import logging

@app.route('/login', methods=['get', 'post'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if (user is None) or (not user.check_password(form.password.data)):
            flash('Connexion impossible. Veuillez vérifier votre nom d\'utilisateur et mot de passe', 'danger')
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
        UserDataAccess.addUser(
            form.username.data, 
            form.password.data, 
            form.firstname.data,
            form.lastname.data,
            form.birthday.data,
            form.email.data)
        flash('Votre compte à été créé, vous pouvez maintenant vous connecter', 'success')
        return redirect(url_for('login'))
    return render_template('login/registration.html.j2', title='Register', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
