from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user
from ..forms import CommentForm, PostForm, RegistrationForm
from ..models import Post, User, Comment
from datetime import datetime

import io
import base64

socials = Blueprint('socials', __name__)

@socials.route('/about', methods=["GET"])
def about():
    return render_template('about.html')

@socials.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()

    if form.validate_on_submit() and current_user.is_authenticated:
        Post(poster=current_user._get_current_object(), title=form.title.data,
            content=form.text.data, calories=form.calories.data).save()
        return redirect(url_for("socials.index"))
    
    posts = Post.objects()

    return render_template("index.html", form=form, posts=posts)

@socials.route('/posts/<post_id>', methods=["GET", "POST"])
def post_detail(post_id: str):
    form = CommentForm()
    post = Post.objects(id=post_id).first()
    
    if form.validate_on_submit() and current_user.is_authenticated:
        print("We out here")
        Comment(commenter=current_user._get_current_object(), content=form.text.data, 
            parent=post_id, post=post, date=datetime.now().strftime("%B %d, %Y at %H:%M:%S")).save()
        return redirect(url_for('socials.post_detail', post_id=post_id))

    comments = Comment.objects(post=post)
    print(comments)
    return render_template('post_detail.html', post = post, form=form, comments=comments)


@socials.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    posts = Post.objects(poster=user)

    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()

    return render_template("user_detail.html", username=username, posts=posts, image = image)
