import unittest
from datetime import datetime, timezone, timedelta
from app import create_app
from app.extensions import db
from app.models import User, Post, Category, Tag


class SearchFilterTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Seed author
        self.author = User(username='search_author', email='sa@example.com')
        self.author.set_password('pass123')
        db.session.add(self.author)

        # Categories
        self.cat_python = Category(name='Python Dev', slug='python-dev')
        self.cat_frontend = Category(name='Frontend Design', slug='frontend-design')
        db.session.add_all([self.cat_python, self.cat_frontend])

        # Tags
        self.tag_flask = Tag(name='Flask', slug='flask')
        self.tag_css = Tag(name='CSS', slug='css')
        db.session.add_all([self.tag_flask, self.tag_css])
        db.session.commit()

        # Posts
        now = datetime.now(timezone.utc)
        self.post1 = Post(
            title='Mastering Flask Web Development',
            slug='mastering-flask-web-development',
            summary='Building REST APIs and web apps.',
            content='Flask is lightweight and flexible for Python engineers.',
            author=self.author,
            category=self.cat_python,
            tags=[self.tag_flask],
            created_at=now - timedelta(days=2)
        )
        self.post2 = Post(
            title='Bootstrap 5 Grid System Secrets',
            slug='bootstrap-5-grid-system-secrets',
            summary='Responsive design tips and flexbox.',
            content='Clean responsive websites with modern CSS utility classes.',
            author=self.author,
            category=self.cat_frontend,
            tags=[self.tag_css],
            created_at=now - timedelta(days=1)
        )
        self.post3 = Post(
            title='SQLAlchemy Advanced Relationships',
            slug='sqlalchemy-advanced-relationships',
            summary='ORM performance and lazy loading.',
            content='Deep dive into join conditions and composite keys in Python.',
            author=self.author,
            category=self.cat_python,
            tags=[self.tag_flask],
            created_at=now
        )
        db.session.add_all([self.post1, self.post2, self.post3])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_search_by_title(self):
        """Test searching articles by title keyword."""
        response = self.client.get('/search?q=Bootstrap')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bootstrap 5 Grid System Secrets', response.data)
        self.assertNotIn(b'SQLAlchemy Advanced Relationships', response.data)

    def test_search_by_content(self):
        """Test searching articles by content keyword."""
        response = self.client.get('/search?q=lightweight')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Mastering Flask Web Development', response.data)

    def test_filter_by_category(self):
        """Test filtering articles by category slug."""
        response = self.client.get('/search?category=frontend-design')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bootstrap 5 Grid System Secrets', response.data)
        self.assertNotIn(b'Mastering Flask Web Development', response.data)

    def test_filter_by_tag(self):
        """Test filtering articles by tag slug."""
        response = self.client.get('/search?tag=css')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bootstrap 5 Grid System Secrets', response.data)
        self.assertNotIn(b'SQLAlchemy Advanced Relationships', response.data)

    def test_sort_newest_vs_oldest(self):
        """Test sorting articles by date ascending and descending."""
        # Oldest first: post1 should appear before post3
        resp_oldest = self.client.get('/search?sort=oldest')
        self.assertEqual(resp_oldest.status_code, 200)
        idx_post1 = resp_oldest.data.find(b'Mastering Flask Web Development')
        idx_post3 = resp_oldest.data.find(b'SQLAlchemy Advanced Relationships')
        self.assertTrue(idx_post1 < idx_post3)

        # Newest first: post3 should appear before post1
        resp_newest = self.client.get('/search?sort=newest')
        self.assertEqual(resp_newest.status_code, 200)
        idx_post1_new = resp_newest.data.find(b'Mastering Flask Web Development')
        idx_post3_new = resp_newest.data.find(b'SQLAlchemy Advanced Relationships')
        self.assertTrue(idx_post3_new < idx_post1_new)

    def test_empty_search_results(self):
        """Test search returns empty state when no records match."""
        response = self.client.get('/search?q=NonExistentKeywordXYZ')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No articles match your criteria', response.data)


if __name__ == '__main__':
    unittest.main()
