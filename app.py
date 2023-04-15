"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'welfknlewnf'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    db.create_all()

@app.route('/')
def home_page():
    """Redirect to list of users."""

    pass

@app.route('/users')
def get_users():
    """Show all users. Make these links to view the detail page for the user. Have a link here to the add-user form."""
    
    users = User.query.all()
    return render_template('users.html', users = users)

@app.route('/users/new')
def add_user():
    """Show an add form for users"""

    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def process_new_user():
    # Process the add form, adding a new user and going back to /users

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image-url']

    user = User(first_name = first_name, last_name = last_name)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def get_user_by_id(user_id):
    # Show information about the given user. Have a button to get to their edit page, and to delete the user.
    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user = user)

@app.route('/users/<int:user_id>/edit')
def edit_user_by_id(user_id):
    # Show the edit page for a user. Have a cancel button 
    # that returns to the detail page for a user, and a save button that updates the user.
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user = user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def process_edited_user(user_id):
    # Process the edit form, returning the user to the /users page.
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image-url']

    db.session.add(user)
    db.session.commit()
    print('==============route called===============')
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user_by_id(user_id):
    #  Delete the user.

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')