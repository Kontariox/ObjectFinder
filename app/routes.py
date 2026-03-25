from flask import Blueprint, render_template, request
from .vehicle import vehicle

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html", vehicle=vehicle)

@main.route("/control", methods=["POST"])
def control():
    action = request.form.get("action")

    if action == "forward":
        # do przodu
        pass #do usuniecia
    elif action == "backward":
        # do tylu
        pass #do usuniecia
    elif action == "left":
        #lewo
        pass #do usuniecia
    elif action == "right":
        #prawo
        pass #do usuniecia

    return render_template("index.html", vehicle=vehicle)