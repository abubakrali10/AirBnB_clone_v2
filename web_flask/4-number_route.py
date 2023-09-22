#!/usr/bin/python3
"""initializes a Flask web application"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """displays Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """displays HBNB"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_isfun(text):
    """displays a variable content"""
    new_text = text.replace('_', ' ')
    return 'C ' + new_text


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python', strict_slashes=False)
def python_isfun(text="is cool"):
    """displays a variable content"""
    new_text = text.replace('_', ' ')
    return 'Python ' + new_text


@app.route('/number/<int:n>', strict_slashes=False)
def is_integer(n):
    """display only if n is integer"""
    if isinstance(n, int):
        return f"{n} is a number"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
