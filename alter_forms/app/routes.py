from app import app
from flask import render_template, redirect, url_for, flash, request

from app.forms import MyLoginForm

from app.models import User
# create five users with ids 1 to 5     
users = [User(id) for id in range(1, 5)]

@app.route('/')
def main( ):
    return render_template('index.html', user=request.args.get('_user'))

@app.route('/login', methods=['get', 'post'])
def login():
    
    form = MyLoginForm()
    if form.validate_on_submit(): # check if it is a POST request and if it is valid.

        user_found = False;
        for n in range(0, len(users)):
            if( users[n].getName() == form.username.data ):
                user_found = True;
                break;
            
        if user_found:
            if (form.password.data == form.username.data + "_secret"):
                return redirect(url_for('main', _user=form.username.data))
            else:
                flash('Wrong password','danger') # error message plus category
                return redirect(url_for('login'))
        else:
            flash('Wrong username','danger')
            return redirect(url_for('login'))
    else:
        return render_template('my_login_form.html', form = form)

    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/page_a')
def page_a():
    return render_template('page_a.html')

@app.route('/page_b')
def page_b():
    return render_template('page_b.html')

