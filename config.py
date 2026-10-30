import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')


class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-secret-key-replace-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = int(os.environ.get('POSTS_PER_PAGE', 6))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max payload
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', f'sqlite:///{BASE_DIR / "instance" / "blog_dev.db"}'
    )


from sqlalchemy.pool import StaticPool


class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    DEBUG = False
    WTF_CSRF_ENABLED = False  # Facilitates automated form testing
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'poolclass': StaticPool,
        'connect_args': {'check_same_thread': False}
    }
    POSTS_PER_PAGE = 4


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    ENV = 'production'
    # Fallback to local SQLite in instance dir if not explicitly set
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', f'sqlite:///{BASE_DIR / "instance" / "blog_prod.db"}'
    )


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
