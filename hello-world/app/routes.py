from app import app
from flask import render_template, redirect
from flask import url_for, request

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/hello_world_one")
def hello_world_one():
    return """
        <!DOCTYPE html>
        <html>
            <head><title>Hello</title></head>
            <body><h1>Hello World One</h1></body>
        </html>
    """, 200

@app.route("/hello_world_two/<username>")
def hello_world(username):
    return "Hello {}".format(username)

@app.route("/hello_world_six")
def index(name="", surname=""):
    name = request.args.get("name")
    surname = request.args.get("surname")
    return """
        You entered a query string with the name of {} {}, and
        request.args.get returned it as a {} of course!
    """.format(name, surname, type(name).__name__)

@app.route("/hello_world_template")
def hello_template():
    return render_template("hello.html")

@app.route("/process_request", methods=['GET', 'POST'])
def process_request():
    if request.method == 'POST':
        _username = request.form['username']
        if _username:
            return render_template('response.html', username=_username)
        else:
            return 'Please go back and enter your name', 400
    else:
        return render_template('form.html')