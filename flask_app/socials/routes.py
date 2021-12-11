from flask import Blueprint, redirect, url_for, render_template
from ..forms import SearchForm, RegistrationForm
from ..models import User, Comment

socials = Blueprint('socials', __name__)

# INCOMPLETE
# The user's feed, which displays their friends' posts in chronological order and lets them search for 
# other users by username
@socials.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("socials.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)
