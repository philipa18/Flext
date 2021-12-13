from flask import Blueprint, redirect, url_for, render_template, flash, request, session
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message

from .. import bcrypt
from .. import oauth
from .. import mail
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm
from ..models import User

users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = RegistrationForm()
    if form.validate_on_submit():
        msg = Message('Hello, Thank you for joining our app', sender = 'cmsc388jfinal@gmail.com' , recipients = [form.email.data])
        mail.send(msg)
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()

        return redirect(url_for("users.login"))

    return render_template("register.html", title="Register", form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user)
            return redirect(url_for("users.account"))
        else:
            flash("Login failed. Check your username and/or password")
            return redirect(url_for("users.login"))

    return render_template("login.html", title="Login", form=form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("users.register"))

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    username_form = UpdateUsernameForm()

    if username_form.validate_on_submit():
        # current_user.username = username_form.username.data
        current_user.modify(username=username_form.username.data)
        current_user.save()
        return redirect(url_for("users.account"))

    return render_template(
        "account.html",
        title="Account",
        username_form=username_form,
    )


@users.route('/google_login')
def google_login():
    google = oauth.create_client('google')  
    redirect_uri = url_for('users.google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@users.route('/google_authorize')
def google_authorize():
    google = oauth.create_client('google')  
    token = google.authorize_access_token()  
    resp = google.get('userinfo')  
    user_info = resp.json()
    user = oauth.google.userinfo()  

    username= user['family_name'] + user['given_name'] 
    email=user['email']

    user = User.objects(username = username, email=user['email'], password = '').first()
    if user is not None:
        login_user(user)
    else:
        user = User(username= username, email=email, password = '')
        user.save()
        msg = Message('Hello, Thank you for joining our app', sender = 'cmsc388jfinal@gmail.com' , recipients = [email])
        mail.send(msg)
        login_user(user)


    session['profile'] = user_info
    session.permanent = True  
    return redirect('users.account')


