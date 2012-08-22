from flask import Flask,render_template
from blog import app

@app.errorhandler(404)
def page_not_found(e):
    return 'Template not found', 404
