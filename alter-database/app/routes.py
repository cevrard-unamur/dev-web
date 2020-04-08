from app import app
from flask import render_template, redirect, url_for, flash, request

from app.forms import MyLoginForm
from app.forms import MyRegistrationForm
from app.forms import ShortMessageForm

from app import db

from werkzeug.urls import url_parse
from app.models import User, Short_messages
from flask_login import login_required, login_user, logout_user, current_user

from flask_login import LoginManager, login_required, login_user, logout_user, current_user

@app.route('/')
@login_required
def main():
    return render_template('index.html')
      
@app.route('/login', methods=['get', 'post'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    
    form = MyLoginForm()
    if form.validate_on_submit(): # check if it is a POST request and if it is valid.
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('You are not registered yet', 'info')
            return redirect(url_for('login'))
        elif not user.check_password(form.password.data):
            flash('Invalid username or password', 'info')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main')
        return redirect(next_page)
    else:
        return render_template('my_login_form.html', form = form)

    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = MyRegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'info')
        return redirect(url_for('login'))
    return render_template('my_registration_form.html', title='Register', form=form)


@app.route('/drop_message', methods=['GET', 'POST'])
@login_required
def drop_message():
    form = ShortMessageForm()
    if form.validate_on_submit():
        short_text = Short_messages ( text=form.text.data, author = current_user )
        db.session.add(short_text)
        db.session.commit()
        flash('Congratulations, your message has been successfully registered !!! ', 'info')
        return redirect(url_for('main'))
    else:
        return render_template('drop_message.html', form = form)

    
@app.route('/show_messages')
@login_required
def show_messages():
    text_list = Short_messages.query.filter_by( users_id=current_user.get_id() ).all()
    return render_template('show_short_messages.html', text_list = text_list )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.route('/page_a')
@login_required
def page_a():
    return render_template('page_a.html')

@app.route('/page_b')
@login_required
def page_b():
    return render_template('page_b.html')

