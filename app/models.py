from datetime import datetime, timezone
import hashlib
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager
from app.utils import slugify, calculate_reading_time


# Association table for Many-to-Many relationship between Post and Tag
post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    bio = db.Column(db.String(500), default='Passionate writer and reader.')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password: str):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify user password."""
        return check_password_hash(self.password_hash, password)

    def avatar(self, size: int = 80) -> str:
        """Generate Gravatar URL from email hash or fallback to UI Avatars."""
        email_clean = self.email.strip().lower().encode('utf-8')
        digest = hashlib.md5(email_clean).hexdigest()
        # Gravatar with fallback to UI avatars styled dynamically
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    @property
    def initial(self) -> str:
        """Get first uppercase letter of username for avatar badge."""
        return self.username[0].upper() if self.username else 'U'

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user loader callback."""
    return db.session.get(User, int(user_id))


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)

    # Relationships
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __init__(self, name, description=None, slug=None):
        self.name = name
        self.description = description
        self.slug = slug or slugify(name)

    @property
    def post_count(self) -> int:
        return self.posts.count()

    def __repr__(self):
        return f'<Category {self.name}>'


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(60), unique=True, nullable=False, index=True)

    # Relationships
    posts = db.relationship(
        'Post',
        secondary=post_tags,
        back_populates='tags',
        lazy='dynamic'
    )

    def __init__(self, name, slug=None):
        self.name = name
        self.slug = slug or slugify(name)

    @property
    def post_count(self) -> int:
        return self.posts.count()

    def __repr__(self):
        return f'<Tag {self.name}>'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(250), unique=True, nullable=False, index=True)
    summary = db.Column(db.String(350), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET NULL'), nullable=True, index=True)

    # Relationships
    tags = db.relationship(
        'Tag',
        secondary=post_tags,
        back_populates='posts'
    )
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan', order_by='Comment.created_at.desc()')

    @property
    def reading_time(self) -> int:
        """Estimated reading time in minutes."""
        return calculate_reading_time(self.content)

    @property
    def clean_excerpt(self) -> str:
        """Generate a clean plain text excerpt if summary is empty."""
        if self.summary:
            return self.summary
        import re
        plain = re.sub(r'<[^>]*?>', ' ', self.content or '')
        clean = ' '.join(plain.split())
        return clean[:160] + ('...' if len(clean) > 160 else '')

    def __repr__(self):
        return f'<Post {self.title}>'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, index=True)

    def __repr__(self):
        return f'<Comment {self.id} on Post {self.post_id}>'
