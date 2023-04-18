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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    

def connect_db(app):
    db.app = app
    db.init_app(app)