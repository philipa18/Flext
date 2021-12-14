from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from . import config
import base64

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

# INCOMPLETE -- ADD MORE INSTANCE VARIABLES IF NECESSARY
# A User consists of a unique username, email, and password
class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=False)
    profile_pic = db.ImageField()
    weight = db.IntField(required=False)
    

    # Returns a unique string (the user's username) identifying each user
    def get_id(self):
        return self.username

class Post(db.Document):
    title = db.StringField(required=True, min_length=1, max_length=50)
    content = db.StringField(required=True, min_length=1, max_length=500)
    calories = db.IntField()
    poster = db.ReferenceField(User, required=True)
    pumps = db.IntField()

class Comment(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=1, max_length=250)
    date = db.StringField(required=True)
    parent = db.StringField(Required=False)
    post = db.ReferenceField(Post, required=False)


