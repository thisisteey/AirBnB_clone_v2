#!/usr/bin/python3
"""Script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)
"""Flask application instance is defined"""
app.url_map.strict_slashes = False


@app.route("/states")
@app.route("/states/<id>")
def states_and_id(id=None):
    """The states page displays HTML page of state info"""
    sorted_states = sorted(storage.all(State).values(), key=lambda x: x.name)
    case = 404
    if id is not None:
        exp = list(filter(lambda x: x.id == id, sorted_states))
        if len(exp) > 0:
            state = exp[0]
            state.cities.sort(key=lambda x: x.name)
            case = 2
            return render_template("9-states.html", state=state, case=case)
    else:
        states = sorted_states
        for state in states:
            state.cities.sort(key=lambda x: x.name)
        states.sort(key=lambda x: x.name)
        case = 1
        return render_template("9-states.html", states=states, case=case)
    return render_template("9-states.html", case=case)


@app.teardown_appcontext
def teardown_flask(exc):
    """The Flask context end listener"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
