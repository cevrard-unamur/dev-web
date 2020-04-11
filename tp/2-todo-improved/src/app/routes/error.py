from app import app
from flask import render_template

# Page 404 retournée si l'URL entrée par l'utilisateur n'est pas connue
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html.j2'), 404