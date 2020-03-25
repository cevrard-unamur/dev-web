from app import app
import os
import urllib.request
from flask import render_template, redirect
from flask import url_for, request
from flask import send_from_directory
from app.upload_file import allowed_file
from werkzeug.utils import secure_filename

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.base_url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.base_url)
        if file and allowed_file(file.filename):
            _filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], _filename))
            return redirect(url_for('uploaded_file', filename=_filename))
    else:
        return render_template('404.html')

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/form", methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template("form.html")
    if request.method == 'POST':
        _name = request.form['name']
        _surname = request.form['surname']
        _birthday = request.form['birthday']
        _nationality = request.form['nationality']
        return render_template("form-response.html", name=_name, surname=_surname, birthday=_birthday, nationality=_nationality)
    else:
         render_template("404.html")