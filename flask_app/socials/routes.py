from flask import Blueprint, render_template

socials = Blueprint('socials', __name__)

# a simple page that says hello
@socials.route('/', methods=['GET'])
def index():
    return render_template("index.html")