from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user
from ..forms import PostForm, RegistrationForm
from ..models import Post, User, Comment

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
    return render_template('post_detail.html', post = Post.objects(id=post_id).first())
