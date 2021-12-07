from flask import Blueprint

socials = Blueprint('socials', __name__)

# a simple page that says hello
@socials.route('/', methods=['GET'])
def index():
    return 'Hello, World!'