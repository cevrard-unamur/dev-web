from app import app

from flask import render_template, redirect, url_for, flash
from app.forms import MyLoginForm


from app.models import User
# create some users with ids 1 to 5     
users = [User(id) for id in range(1, 5)]

from flask_login import login_required, login_user, logout_user, current_user

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

        user_found = False;
        for n in range(0, len(users)): # print(users[n].getId())
            if( users[n].getName() == form.username.data ):
                user_found = True;
                break;
            
        if user_found:
            if (form.password.data == form.username.data + "_secret"):
                id = form.username.data.split('user')[1]
                user = User(id)
                login_user(user)
                return redirect(url_for('main'))
            else:
                flash('Wrong password','danger') # error message plur category
                return redirect(url_for('login'))
        else:
            flash('Wrong username','danger') # error message plur category
            return redirect(url_for('login'))
    else:
        return render_template('my_login_form.html', form = form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/logout')
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
