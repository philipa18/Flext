from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from authlib.integrations.flask_client import OAuth
from flask_mail import Mail
from flask_talisman import Talisman
# stdlib
from datetime import datetime
import os

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
oauth = OAuth()
mail = Mail()

def page_not_found(e):
    return render_template("404.html"), 404

def create_app(test_config=None):
    app = Flask(__name__)
    
    csp = {
        'default-src': ['\'self\'', '\'unsafe-inline\'', 'stackpath.bootstrapcdn.com', 'code.jquery.com', 'cdn.jsdelivr.net'],
        'img-src': ['\'self\'', 'data:']
    }    
    Talisman(app, content_security_policy=csp)

    app.config["MONGODB_HOST"] = os.getenv("MONGODB_HOST") # Heroku database setup

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = '465'
    app.config['MAIL_USERNAME'] = 'cmsc388jfinal@gmail.com'
    app.config['MAIL_PASSWORD'] = 'cs388jfinal'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    


    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    oauth.init_app(app)
    mail.init_app(app)

    app.register_blueprint(socials)
    app.register_blueprint(users)
    app.register_error_handler(404, page_not_found)

    google = oauth.register(
    name='google',
    client_id='57278910420-pr482i5gjgfk4fm98d37s8frkflckkef.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
    )


    return app

# Blueprints
from .socials.routes import socials
from .users.routes import users
