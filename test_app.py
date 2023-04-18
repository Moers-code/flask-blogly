from unittest import TestCase
from app import app
from models import User, Post
from database import db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SQLALCHEMY_ECHO'] = False

with app.app_context():
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

                # post = Post(title='test', content='Testing Posts', user_id = self.user_id)
                # db.session.add(post)
                # db.session.commit()
                # self.post_id = post.id 
    
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

            res = client.post('/users/1/delete')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/users')
            user = User.query.get(1)
            self.assertIsNone(user)

            # Here the post should've been None
            self.assertIsNotNone(post)

        
            

    # def test_add_new_post(self):
    #     with app.test_client() as client:
    #         res = client.post(f'/users/{self.user_id}/posts/new', data={'title':'second test', 'content': 'nothing to see'})
    #         html = res.get_data(as_text=True)

    #         self.assertEqual(res.status_code, 302)