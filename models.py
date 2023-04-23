"""Models for Blogly."""
from datetime import datetime
from database import db

default_icon = src="https://www.freeiconspng.com/uploads/profile-icon--golden-control-icons--softiconsm-18.png"

class User(db.Model):
    """User"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    
    first_name = db.Column(db.String(20),
                            nullable = False
                            )

    last_name = db.Column(db.String(20),
                            nullable = False)
    
    image_url = db.Column(db.Text, nullable = False, default = default_icon)

    post = db.relationship('Post', backref = 'user', cascade="all, delete-orphan")
                            
class Post(db.Model):
    """Posts Table"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    title = db.Column(db.Text,
                        nullable = False)
    
    content = db.Column(db.Text,
                        nullable = False)
    
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    tags = db.relationship('Tag', secondary = 'posts_tags', backref = 'posts')
    

    
class Tag(db.Model):
    """Tags Table"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, nullable = False, unique=True)

class PostTag(db.Model):
    """PostTag Table"""

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)


def connect_db(app):
    db.app = app
    db.init_app(app)