#!/usr/bin/python3
"""Script that starts a Flask web application"""
from flask import Flask


app = Flask(__name__)
"""Flask application instance is defined"""
app.url_map.strict_slashes = False


@app.route("/")
def home():
    """The home page message"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
