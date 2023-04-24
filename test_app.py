from unittest import TestCase
from app import app
from models import User, Post, connect_db, Tag
from database import db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SQLALCHEMY_ECHO'] = False

with app.app_context():
    connect_db(app)
    db.drop_all()
    db.create_all()

class BloglyTests(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add sample user"""
        with app.app_context():
            User.query.delete()
            Post.query.delete()
            with app.app_context():
                user = User(first_name='Mo', last_name='Jo')
                db.session.add(user)
                db.session.commit()
                self.user_id = user.id
    
    def tearDown(self):
        """Clean Up"""

        with app.app_context():
            db.session.rollback()

    def test_get_users(self):
        with app.test_client() as client:
        
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Mo', html)


    def test_process_new_user(self):
        with app.test_client() as client:
            
            res = client.post('/users/new', data={'first_name': 'Jax', 'last_name':'Yo', 'image-url': ''})
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/users')
            
            res = client.get(res.location)
            html = res.get_data(as_text=True)
            self.assertIn('Jax Yo', html)

    def test_process_edited_user(self):
        with app.test_client() as client:
            res = client.post(f'/users/{self.user_id}/edit', data={'first_name':'edited', 'last_name': 'user', 'image-url': ''})
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/users')

            res = client.get(res.location)
            html = res.get_data(as_text = True)

            self.assertIn('edited', html)


    def test_delete_user(self):
        with app.test_client() as client:
            with app.app_context():
                user = User.query.get(self.user_id)
                post = Post(title='test', content='Testing Posts', user_id = user.id)
                db.session.add(post)
                db.session.commit()

                res = client.post(f'/users/{self.user_id}/delete')
                html = res.get_data(as_text=True)

                self.assertEqual(res.status_code, 302)
                self.assertEqual(res.location, '/users')
                user = User.query.get(self.user_id)
                self.assertIsNone(user)

                post = Post.query.filter_by(id = post.id).first()
                self.assertIsNone(post)

    def test_add_new_post(self):
        with app.test_client() as client:
            with app.app_context():

                res = client.post('/users/1/posts/new', data={'title': 'testing Post', 'content': 'Edit Post in Tests', 'user_id':1})
                html = res.get_data(as_text=True)

                self.assertEqual(res.status_code, 302)
                
    def test_edit_post(self):
        with app.test_client() as client:
            with app.app_context():
                post = Post(title='new Title', content= 'new Content')
                db.session.add(post)
                db.session.commit()

                res = client.post(f'/posts/{post.id}/edit', data={'title': 'testing', 'content': 'testing content'})
                
                self.assertEqual(res.status_code, 302)
                self.assertEqual(res.location, f'/posts/{post.id}')

                res = client.get(res.location)
                html = res.get_data(as_text=True)

                self.assertIn('<p>testing content</p>', html)
                

    def test_delete_post(self):
        with app.test_client() as client:
            with app.app_context():
                post = Post(title='new Title', content= 'new Content', user_id = self.user_id)  
                db.session.add(post)
                db.session.commit()
                
                res = client.post(f'/posts/{post.id}/delete')
                
                self.assertEqual(res.status_code, 302)
                deleted_post = Post.query.filter_by(id = post.id).first()
                self.assertIsNone(deleted_post)
                self.assertEqual(res.location, f'/users/{self.user_id}')
                

    def test_get_tags(self):
        with app.test_client() as client:
            with app.app_context():
                tag = Tag(name = 'new Tag')
                tag_two = Tag(name = 'another Tag')
                db.session.add(tag)
                db.session.add(tag_two)
                db.session.commit()

                res = client.get('/tags')
                html = res.get_data(as_text=True)

                self.assertEqual(res.status_code, 200)
                self.assertIn('new Tag', html)

    
    def test_create_tag(self):
        with app.test_client() as client:
            with app.app_context():
                res = client.post('/tags/new', data={'new_tag':'test tag'})
                

                self.assertEqual(res.status_code, 302)
                self.assertEqual(res.location, '/tags')

                res = client.get('/tags')
                html = res.get_data(as_text=True)

                self.assertEqual(res.status_code, 200)
                self.assertIn('test tag', html)

    def test_edit_tag(self):
        with app.test_client() as client:
            with app.app_context():
                tag = Tag(name = 'new tag')
                db.session.add(tag)
                db.session.commit()

                res = client.post(f'/tags/{tag.id}/edit', data={'edit_tag': 'edited tag'})

                self.assertEqual(res.status_code, 302)
                self.assertEqual(res.location, '/tags')

                res = client.get('/tags')
                html = res.get_data(as_text=True)

                self.assertEqual(res.status_code, 200)
                self.assertIn('edited tag', html)
    
    def test_delete_tag(self):
        with app.test_client() as client:
            with app.app_context():
                test_tag = Tag(name='new test tag')
                db.session.add(test_tag)
                db.session.commit()

                res = client.post(f'tags/{test_tag.id}/delete')

                self.assertEqual(res.status_code, 302)
                self.assertEqual(res.location, '/tags')

                res = client.get('/tags')
                html = res.get_data(as_text=True)

                self.assertEqual(res.status_code, 200)
                self.assertNotIn('new test tag', html)