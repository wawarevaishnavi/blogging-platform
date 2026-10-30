import re
import math
import bleach


# Allowed HTML tags for rich text editor content
ALLOWED_TAGS = [
    'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'strong', 'em', 'u', 's', 'b', 'i', 'strike',
    'blockquote', 'code', 'pre',
    'ul', 'ol', 'li',
    'a', 'span', 'br', 'hr',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'img'
]

# Allowed attributes per tag (safe attributes, no inline javascript or unvetted styles)
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target', 'rel'],
    'span': ['class'],
    'p': ['class'],
    'code': ['class'],
    'pre': ['class'],
    'blockquote': ['class'],
    'img': ['src', 'alt', 'title', 'class'],
    '*': ['class']
}


def sanitize_html(content: str) -> str:
    """
    Sanitize user-submitted HTML to prevent Cross-Site Scripting (XSS) attacks.
    Strips scripts, inline JavaScript handlers, unsafe iframes, etc.
    """
    if not content:
        return ''

    cleaned = bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
    # Automatically add rel="noopener noreferrer" to external links for security
    cleaned = bleach.linkify(cleaned, callbacks=[bleach.callbacks.nofollow])
    return cleaned


def slugify(text: str) -> str:
    """Convert text into a URL-friendly slug."""
    if not text:
        return ''
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text


def calculate_reading_time(html_content: str, words_per_minute: int = 200) -> int:
    """Calculate estimated reading time in minutes from HTML or raw text."""
    if not html_content:
        return 1
    # Strip HTML tags
    clean_text = re.sub(r'<[^>]*?>', ' ', html_content)
    words = re.findall(r'\w+', clean_text)
    word_count = len(words)
    minutes = math.ceil(word_count / max(words_per_minute, 1))
    return max(1, minutes)
