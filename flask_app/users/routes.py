from flask import Blueprint

users = Blueprint('users', __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    return 'The Register Page'