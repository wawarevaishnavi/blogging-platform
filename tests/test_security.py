import unittest
from app import create_app
from app.utils import sanitize_html
from app.routes.auth import is_safe_redirect_url


class SecurityTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_xss_script_tags_stripped(self):
        """Verify that malicious script tags are stripped by Bleach."""
        malicious_input = '<p>Hello world</p><script>alert("XSS Attack!");</script>'
        sanitized = sanitize_html(malicious_input)
        self.assertNotIn('<script>', sanitized)
        self.assertNotIn('</script>', sanitized)
        self.assertIn('<p>Hello world</p>', sanitized)

    def test_xss_onerror_attributes_stripped(self):
        """Verify that inline event handlers like onerror, onclick are stripped."""
        malicious_input = '<img src="invalid.jpg" onerror="alert(document.cookie)">'
        sanitized = sanitize_html(malicious_input)
        self.assertNotIn('onerror', sanitized)
        self.assertNotIn('alert', sanitized)

    def test_safe_rich_text_preserved(self):
        """Verify that valid rich-text formatting tags and code blocks are preserved."""
        safe_input = '<h2>Architecture Overview</h2><p>Here is <strong>bold</strong> and <em>italic</em> text.</p><pre><code>print("Clean")</code></pre>'
        sanitized = sanitize_html(safe_input)
        self.assertIn('<h2>Architecture Overview</h2>', sanitized)
        self.assertIn('<strong>bold</strong>', sanitized)
        self.assertIn('<em>italic</em>', sanitized)
        self.assertIn('<pre><code>print("Clean")</code></pre>', sanitized)

    def test_open_redirect_protection(self):
        """Verify open redirect protection validates URLs strictly."""
        with self.app.test_request_context('http://localhost:5000/login'):
            self.assertTrue(is_safe_redirect_url('/dashboard'))
            self.assertTrue(is_safe_redirect_url('/posts/create'))
            self.assertTrue(is_safe_redirect_url('http://localhost:5000/posts'))

            # Malicious external redirects must be rejected
            self.assertFalse(is_safe_redirect_url('http://evil-attacker.com'))
            self.assertFalse(is_safe_redirect_url('https://phishing-site.org/fake-login'))
            self.assertFalse(is_safe_redirect_url('//evil.com'))

    def test_404_error_page(self):
        """Verify 404 handler returns clean error template."""
        response = self.client.get('/this-route-does-not-exist-404')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page Not Found', response.data)


if __name__ == '__main__':
    unittest.main()
