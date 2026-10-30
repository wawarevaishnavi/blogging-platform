import unittest
from app import create_app
from app.extensions import db
from app.models import User


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_password_hashing(self):
        """Verify Werkzeug cryptographic password hashing."""
        u = User(username='testuser', email='test@example.com')
        u.set_password('mysecretpass')
        self.assertTrue(u.check_password('mysecretpass'))
        self.assertFalse(u.check_password('wrongpass'))
        self.assertNotEqual(u.password_hash, 'mysecretpass')

    def test_user_registration_success(self):
        """Test successful registration with valid inputs."""
        response = self.client.post('/register', data={
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created successfully', response.data)

        user = User.query.filter_by(username='john_doe').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'john@example.com')

    def test_registration_duplicate_username(self):
        """Test registration validation blocks duplicate username."""
        u = User(username='existing_user', email='first@example.com')
        u.set_password('pass123')
        db.session.add(u)
        db.session.commit()

        response = self.client.post('/register', data={
            'username': 'existing_user',
            'email': 'second@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertIn(b'This username is already taken', response.data)

    def test_registration_duplicate_email(self):
        """Test registration validation blocks duplicate email."""
        u = User(username='first_user', email='duplicate@example.com')
        u.set_password('pass123')
        db.session.add(u)
        db.session.commit()

        response = self.client.post('/register', data={
            'username': 'second_user',
            'email': 'duplicate@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertIn(b'An account with this email already exists', response.data)

    def test_registration_password_mismatch(self):
        """Test registration validation fails when passwords mismatch."""
        response = self.client.post('/register', data={
            'username': 'mismatch_user',
            'email': 'mismatch@example.com',
            'password': 'password123',
            'confirm_password': 'different_password'
        })
        self.assertIn(b'Passwords must match', response.data)

    def test_login_and_logout(self):
        """Test successful user login and logout flow."""
        u = User(username='login_tester', email='login@example.com')
        u.set_password('securepassword')
        db.session.add(u)
        db.session.commit()

        # Login with username
        response = self.client.post('/login', data={
            'email_or_username': 'login_tester',
            'password': 'securepassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back, login_tester', response.data)
        self.assertIn(b'Author Dashboard', response.data)

        # Logout
        logout_resp = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(logout_resp.status_code, 200)
        self.assertIn(b'You have been logged out successfully', logout_resp.data)

    def test_login_invalid_credentials(self):
        """Test login fails with incorrect password."""
        u = User(username='valid_user', email='user@example.com')
        u.set_password('rightpassword')
        db.session.add(u)
        db.session.commit()

        response = self.client.post('/login', data={
            'email_or_username': 'valid_user',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertIn(b'Invalid username/email or password', response.data)

    def test_protected_routes_require_login(self):
        """Test unauthenticated access to dashboard redirects to login."""
        response = self.client.get('/dashboard', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])


if __name__ == '__main__':
    unittest.main()
