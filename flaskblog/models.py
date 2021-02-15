from flaskblog import db, login_manager
import datetime
from flask_login import UserMixin
# hold the models for the database

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # there will be a default profile image
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    # there will be a default profile image
    password = db.Column(db.String(60), nullable=False)
    # backref -> adding a virtuell column to the Post model -> access author by post.author
    posts = db.relationship('Post', backref='author', lazy=True)

    # method to print out the user
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    # foreignKey -> relationship to User.id
    # user and not User like Post above because the column and not the model is meant
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # method to print out the user
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
