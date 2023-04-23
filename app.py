"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from models import connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

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

    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    #  Delete the user.

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def new_post_page(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('add_post.html', user = user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
    user = User.query.get_or_404(user_id)

    title = request.form['title']
    content = request.form['content']
    tag_group = request.form.getlist('tags_group')
    
    post = Post(title = title, content = content, user_id=user_id)

    for tag_name in tag_group:
        tag = Tag.query.filter_by(name = tag_name).first()
        post.tags.append(tag)

    db.session.add(post)
    db.session.commit()
    
    return redirect(f'/users/{user.id}')

@app.route('/posts/<int:post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    print(tags)
    return render_template('post_details.html', post = post, tags = tags)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    return render_template('edit_post.html', post = post)


@app.route('/posts/<int:post_id>/edit', methods=['POST']) 
def edit_post(post_id):
    """ Handle editing of a post. Redirect back to the post view."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete the post."""
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/tags')
def get_tags():
    tags = Tag.query.all()
    return render_template('list_tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('show_tag.html', tag=tag)

@app.route('/tags/new', methods=['GET'])
def new_tag():
    return render_template('create_tag.html')

@app.route('/tags/new', methods=['POST'])
def create_tag():
    tag_name = request.form['new_tag']

    tag = Tag.query.filter_by(name = tag_name).first()

    if tag is None:

        tag = Tag(name = tag_name)
        db.session.add(tag)
        db.session.commit()
    
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form['edit_tag']
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')