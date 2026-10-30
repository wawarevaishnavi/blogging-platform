import unittest
from app import create_app
from app.extensions import db
from app.models import User, Post, Category, Tag


class PostCRUDTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create two test users
        self.user1 = User(username='author1', email='author1@example.com')
        self.user1.set_password('pass123')
        self.user2 = User(username='author2', email='author2@example.com')
        self.user2.set_password('pass123')
        db.session.add_all([self.user1, self.user2])

        # Create a test category
        self.category = Category(name='Technology', description='Tech articles')
        db.session.add(self.category)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username='author1', password='pass123'):
        return self.client.post('/login', data={
            'email_or_username': username,
            'password': password
        }, follow_redirects=True)

    def test_create_post_success(self):
        """Test authenticated post creation with category and tags."""
        self.login('author1', 'pass123')
        response = self.client.post('/posts/create', data={
            'title': 'Architecting Flask Microservices',
            'summary': 'A guide to Flask microservices.',
            'category_id': self.category.id,
            'tags': 'Flask, Architecture, Python',
            'content': '<p>This is a detailed article on Flask microservices.</p>'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your blog post has been published successfully', response.data)

        # Verify in database
        post = Post.query.filter_by(slug='architecting-flask-microservices').first()
        self.assertIsNotNone(post)
        self.assertEqual(post.author.username, 'author1')
        self.assertEqual(post.category.name, 'Technology')
        self.assertEqual(len(post.tags), 3)

    def test_create_post_unauthenticated_redirects(self):
        """Test unauthenticated user cannot access post creation."""
        response = self.client.get('/posts/create', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_read_posts_and_detail(self):
        """Test reading all posts and individual post detail page."""
        post = Post(
            title='Learning Python Basics',
            slug='learning-python-basics',
            content='<p>Python is clean and elegant.</p>',
            user_id=self.user1.id,
            category_id=self.category.id
        )
        db.session.add(post)
        db.session.commit()

        # Read all posts
        resp_all = self.client.get('/posts')
        self.assertEqual(resp_all.status_code, 200)
        self.assertIn(b'Learning Python Basics', resp_all.data)

        # Read detail page
        resp_detail = self.client.get(f'/posts/{post.slug}')
        self.assertEqual(resp_detail.status_code, 200)
        self.assertIn(b'Learning Python Basics', resp_detail.data)
        self.assertIn(b'Python is clean and elegant.', resp_detail.data)

    def test_update_post_by_owner(self):
        """Test that the post owner can update post fields."""
        post = Post(
            title='Original Title',
            slug='original-title',
            content='<p>Original content.</p>',
            user_id=self.user1.id,
            category_id=self.category.id
        )
        db.session.add(post)
        db.session.commit()

        self.login('author1', 'pass123')
        response = self.client.post(f'/posts/{post.id}/edit', data={
            'title': 'Updated Title',
            'summary': 'Updated summary.',
            'category_id': self.category.id,
            'tags': 'UpdatedTag',
            'content': '<p>Updated content successfully.</p>'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your blog post has been updated successfully', response.data)

        updated_post = db.session.get(Post, post.id)
        self.assertEqual(updated_post.title, 'Updated Title')
        self.assertIn('Updated content', updated_post.content)

    def test_update_post_unauthorized_user_forbidden(self):
        """Test that a non-owner attempting to edit a post receives 403 Forbidden."""
        post = Post(
            title='User1 Private Post',
            slug='user1-private-post',
            content='<p>Secret content.</p>',
            user_id=self.user1.id,
            category_id=self.category.id
        )
        db.session.add(post)
        db.session.commit()

        # Login as user2 (not the owner)
        self.login('author2', 'pass123')
        response = self.client.post(f'/posts/{post.id}/edit', data={
            'title': 'Malicious Edit',
            'category_id': self.category.id,
            'content': '<p>Hacked content</p>'
        })
        self.assertEqual(response.status_code, 403)

    def test_delete_post_by_owner(self):
        """Test post owner can successfully delete their post."""
        post = Post(
            title='Post to Delete',
            slug='post-to-delete',
            content='<p>Goodbye post.</p>',
            user_id=self.user1.id,
            category_id=self.category.id
        )
        db.session.add(post)
        db.session.commit()
        post_id = post.id

        self.login('author1', 'pass123')
        response = self.client.post(f'/posts/{post_id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Blog post has been deleted successfully', response.data)

        # Confirm deleted from DB
        self.assertIsNone(db.session.get(Post, post_id))

    def test_delete_post_unauthorized_user_forbidden(self):
        """Test non-owner cannot delete another user's post."""
        post = Post(
            title='User1 Post Safe',
            slug='user1-post-safe',
            content='<p>Content.</p>',
            user_id=self.user1.id,
            category_id=self.category.id
        )
        db.session.add(post)
        db.session.commit()

        self.login('author2', 'pass123')
        response = self.client.post(f'/posts/{post.id}/delete')
        self.assertEqual(response.status_code, 403)
        self.assertIsNotNone(db.session.get(Post, post.id))


if __name__ == '__main__':
    unittest.main()
