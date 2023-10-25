"""
app.py - Basic Flask Application

This is a basic Flask application that serves an index page using a template.
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    """
    Route to display the index page.

    :return: Rendered HTML template (index.html) as the response.
    """
    return render_template('index.html')
