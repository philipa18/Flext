from flask import Blueprint, redirect, url_for, render_template, flash, request, session
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message
from werkzeug.utils import secure_filename


from .. import bcrypt
from .. import oauth
from .. import mail
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm, UpdateWeightForm
from ..models import User, load_user

import io
import base64
import random

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
    UpdateUsername_form = UpdateUsernameForm()
    UpdatePropic_form = UpdateProfilePicForm()
    UpdateWeight_form = UpdateWeightForm()


    if UpdateUsername_form.validate_on_submit():
        new_username = UpdateUsername_form.username.data
        current_user.modify(username=new_username)
        current_user.save()
        logout_user()
        return redirect(url_for('users.login'))

    if UpdateWeight_form.validate_on_submit():
        new_weight= UpdateWeight_form.weight.data
        current_user.modify(weight=new_weight)
        current_user.save()
        return redirect(url_for('users.account'))


    if UpdatePropic_form.validate_on_submit():
        img = UpdatePropic_form.picture.data
        filename = secure_filename(img.filename)
        content_type = f'images/{filename[-3:]}'

        if current_user.profile_pic.get() is None:
            current_user.profile_pic.put(img.stream, content_type=content_type)
        else:
            current_user.profile_pic.replace(img.stream, content_type=content_type)
            
        current_user.save()
        return redirect(url_for('users.account'))


    bytes_im = io.BytesIO(current_user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()

    return render_template("account.html", UpdateUsername_form = UpdateUsername_form, UpdatePropic_form = UpdatePropic_form, UpdateWeight_form = UpdateWeight_form,image = image)



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

    user = User.objects(email=user['email'], password = '').first()
    if user is not None:
        login_user(user)
    else:
        while User.objects(username = username).first() is not None:
            username = user['family_name'] + user['given_name'] + str(random.randint(0, 1000))

        user = User(username= username, email=email, password = '')
        user.save()
        msg = Message('Hello, Thank you for joining our app', sender = 'cmsc388jfinal@gmail.com' , recipients = [email])
        mail.send(msg)
        login_user(user)


    session['profile'] = user_info
    session.permanent = True  
    return redirect(url_for("users.account"))


