#!/usr/bin/python3
"""Script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place


app = Flask(__name__)
"""Flask application instance is defined"""
app.url_map.strict_slashes = False


@app.route("/hbnb")
def hbnb():
    """The hbnb page that displays an HTML page with place info"""
    sorted_states = sorted(storage.all(State).values(), key=lambda x: x.name)
    amenities = sorted(storage.all(Amenity).values(), key=lambda x: x.name)
    places = sorted(storage.all(Place).values(), key=lambda x: x.name)
    for state in sorted_states:
        state.cities.sort(key=lambda x: x.name)
    for place in places:
        place.description = Markup(place.description)
    return render_template("100-hbnb.html", states=sorted_states,
                           amenities=amenities, places=places)


@app.teardown_appcontext
def teardown_flask(exc):
    """The Flask context end listener"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
