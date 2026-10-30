import unittest
from app import create_app
from app.extensions import db
from app.models import User, Post, Category, Comment


class CommentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.post_author = User(username='post_author', email='pa@example.com')
        self.post_author.set_password('pass123')

        self.commenter = User(username='commenter', email='co@example.com')
        self.commenter.set_password('pass123')

        self.intruder = User(username='intruder', email='in@example.com')
        self.intruder.set_password('pass123')

        db.session.add_all([self.post_author, self.commenter, self.intruder])

        self.category = Category(name='DevOps')
        db.session.add(self.category)
        db.session.commit()

        self.post = Post(
            title='Docker Deployment Guide',
            slug='docker-deployment-guide',
            content='<p>Dockerizing Flask apps.</p>',
            user_id=self.post_author.id,
            category_id=self.category.id
        )
        db.session.add(self.post)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password='pass123'):
        return self.client.post('/login', data={
            'email_or_username': username,
            'password': password
        }, follow_redirects=True)

    def test_add_comment_success(self):
        """Test authenticated user can add a comment to a post."""
        self.login('commenter')
        response = self.client.post(f'/posts/{self.post.id}/comment', data={
            'content': 'This Docker tutorial is extremely helpful!'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your comment has been posted', response.data)

        # Verify comment stored in database
        comment = Comment.query.filter_by(post_id=self.post.id).first()
        self.assertIsNotNone(comment)
        self.assertEqual(comment.author.username, 'commenter')
        self.assertEqual(comment.content, 'This Docker tutorial is extremely helpful!')

    def test_add_comment_unauthenticated_redirects(self):
        """Test unauthenticated user cannot submit comment directly."""
        response = self.client.post(f'/posts/{self.post.id}/comment', data={
            'content': 'Unauthorized comment'
        }, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_delete_comment_by_comment_author(self):
        """Test that the commenter can delete their own comment."""
        comment = Comment(
            content='I want to delete this comment.',
            user_id=self.commenter.id,
            post_id=self.post.id
        )
        db.session.add(comment)
        db.session.commit()
        comment_id = comment.id

        self.login('commenter')
        response = self.client.post(f'/comment/{comment_id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comment has been deleted', response.data)
        self.assertIsNone(db.session.get(Comment, comment_id))

    def test_delete_comment_by_post_author(self):
        """Test post owner can moderate/delete any comment on their post."""
        comment = Comment(
            content='Spam comment on post',
            user_id=self.commenter.id,
            post_id=self.post.id
        )
        db.session.add(comment)
        db.session.commit()
        comment_id = comment.id

        # Post author moderating
        self.login('post_author')
        response = self.client.post(f'/comment/{comment_id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(db.session.get(Comment, comment_id))

    def test_delete_comment_unauthorized_forbidden(self):
        """Test third party cannot delete someone else's comment."""
        comment = Comment(
            content='Legitimate discussion',
            user_id=self.commenter.id,
            post_id=self.post.id
        )
        db.session.add(comment)
        db.session.commit()

        # Intruder attempts to delete
        self.login('intruder')
        response = self.client.post(f'/comment/{comment.id}/delete')
        self.assertEqual(response.status_code, 403)
        self.assertIsNotNone(db.session.get(Comment, comment.id))


if __name__ == '__main__':
    unittest.main()
