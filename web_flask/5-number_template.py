#!/usr/bin/python3
"""Script that starts a Flask web application"""
from flask import Flask, render_template


app = Flask(__name__)
"""Flask application instance is defined"""
app.url_map.strict_slashes = False


@app.route("/")
def home():
    """The home page message"""
    return "Hello HBNB!"


@app.route("/hbnb")
def hbnb_page():
    """The HBNB page message"""
    return "HBNB"


@app.route("/c/<text>")
def c_page(text):
    """The C page message displayed by the value of <text>"""
    text = text.replace("_", " ")
    return f"C {text}"


@app.route("/python/<text>")
@app.route("/python", defaults={"text": "is cool"})
def python_page(text):
    """The Python page displayed by the value of <text>"""
    text = text.replace("_", " ")
    return f"Python {text}"


@app.route("/number/<int:n>")
def number_page(n):
    """The number page displayed by n only if it is an integer"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>")
def number_template(n):
    """The number_template page displays HTML pages for integers"""
    return render_template("5-number.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
