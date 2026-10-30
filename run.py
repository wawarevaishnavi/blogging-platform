import os
from app import create_app
from app.extensions import db
from app.models import User, Post, Category, Tag, Comment

app = create_app(os.environ.get('FLASK_CONFIG', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Register database models in the Flask interactive shell."""
    return {
        'db': db,
        'User': User,
        'Post': Post,
        'Category': Category,
        'Tag': Tag,
        'Comment': Comment
    }


def create_tables():
    """Initialize the database tables."""
    with app.app_context():
        db.create_all()
        print('Database tables created successfully.')


def populate_seed():
    """Seed the database with realistic sample categories, users, tags, posts, and comments."""
    from app.utils import slugify, sanitize_html
    from datetime import datetime, timezone, timedelta

    with app.app_context():
        db.drop_all()
        db.create_all()
        print('Clean database tables created.')

        # 1. Create Sample Users
        users_data = [
            {
                'username': 'alex_dev',
                'email': 'alex@example.com',
                'password': 'password123',
                'bio': 'Senior Software Architect passionate about clean code, Flask, and cloud native architectures.'
            },
            {
                'username': 'sarah_tech',
                'email': 'sarah@example.com',
                'password': 'password123',
                'bio': 'Full-stack engineer, Python enthusiast, and technical writer exploring AI & modern web frameworks.'
            },
            {
                'username': 'david_learner',
                'email': 'david@example.com',
                'password': 'password123',
                'bio': 'Computer science student and aspiring backend developer diving deep into database design.'
            }
        ]

        created_users = {}
        for u_data in users_data:
            user = User(
                username=u_data['username'],
                email=u_data['email'],
                bio=u_data['bio']
            )
            user.set_password(u_data['password'])
            db.session.add(user)
            created_users[u_data['username']] = user

        db.session.commit()
        print(f"Created {len(created_users)} demo users.")

        # 2. Create Categories
        categories_data = [
            {'name': 'Web Development', 'description': 'Full-stack development, modern web frameworks, frontend and backend best practices.'},
            {'name': 'Python & Flask', 'description': 'Deep dives into Python programming, Flask architecture, blueprints, and extensions.'},
            {'name': 'Database & SQL', 'description': 'Relational database design, SQLAlchemy ORM patterns, indexing, and performance tuning.'},
            {'name': 'DevOps & Cloud', 'description': 'Continuous integration, containerization, deployment workflows, and cloud environments.'},
            {'name': 'Career & Learning', 'description': 'Tips for software engineering internships, technical interviews, and lifelong learning.'}
        ]

        created_categories = {}
        for c_data in categories_data:
            cat = Category(
                name=c_data['name'],
                description=c_data['description'],
                slug=slugify(c_data['name'])
            )
            db.session.add(cat)
            created_categories[c_data['name']] = cat

        db.session.commit()
        print(f"Created {len(created_categories)} categories.")

        # 3. Create Tags
        tags_data = ['Python', 'Flask', 'SQLAlchemy', 'Bootstrap5', 'REST-API', 'Security', 'Architecture', 'WebDev', 'Tutorial']
        created_tags = {}
        for t_name in tags_data:
            tag = Tag(name=t_name, slug=slugify(t_name))
            db.session.add(tag)
            created_tags[t_name] = tag

        db.session.commit()
        print(f"Created {len(created_tags)} tags.")

        # 4. Create Sample Posts
        posts_data = [
            {
                'title': 'Building Scalable Web Applications with Flask and SQLAlchemy',
                'summary': 'Discover modern architectural patterns for structuring large-scale Flask applications using blueprints and modular services.',
                'content': '''<h2>Introduction to Modular Flask Architecture</h2>
<p>When starting with Flask, it is common to bundle everything into a single <code>app.py</code> file. While this approach works wonders for quick scripts, production systems require a more structured paradigm.</p>
<h3>1. The Application Factory Pattern</h3>
<p>Using an application factory function such as <code>create_app()</code> allows you to create multiple instances of your app with varying configurations—ideal for testing, development, and staging environments.</p>
<blockquote>"Structuring your project with distinct blueprints and clean separation of concerns makes your codebase maintainable and testable."</blockquote>
<h3>2. Relational Modeling with SQLAlchemy</h3>
<p>Flask-SQLAlchemy provides high-level abstractions over SQL, allowing you to define models cleanly with declarative base classes, automated foreign keys, and cascading relationships.</p>
<ul>
<li><strong>Clean decoupling:</strong> Database models remain isolated in their own module.</li>
<li><strong>Type safety & validation:</strong> WTForms and SQLAlchemy guarantee data integrity.</li>
<li><strong>Security:</strong> Parameterized queries prevent SQL injection out of the box.</li>
</ul>
<p>Stay tuned for our deep dive into asynchronous tasks and background workers!</p>''',
                'author': created_users['alex_dev'],
                'category': created_categories['Python & Flask'],
                'tags': [created_tags['Python'], created_tags['Flask'], created_tags['Architecture']],
                'days_ago': 5
            },
            {
                'title': 'Mastering Secure User Authentication in Python Web Apps',
                'summary': 'A comprehensive guide to password hashing with Werkzeug, session protection with Flask-Login, and defending against CSRF.',
                'content': '''<h2>Security First: Building Trust in Your Web Platform</h2>
<p>Authentication is the gateway to your web application. Weak password handling or poor session management puts your entire user base at risk.</p>
<h3>Password Hashing Demystified</h3>
<p>Never store plain text passwords. Using modern hashing algorithms like <em>scrypt</em> or <em>PBKDF2</em> with cryptographic salting ensures that even if database dumps are compromised, credentials remain mathematically secure.</p>
<pre><code>from werkzeug.security import generate_password_hash, check_password_hash

# Generating a cryptographic hash
hashed = generate_password_hash("user_secret_password")
# Verifying securely
is_valid = check_password_hash(hashed, "user_secret_password")
</code></pre>
<h3>Essential Defenses:</h3>
<ol>
<li><strong>CSRF Protection:</strong> Always validate synchronization tokens on all state-altering requests (POST, PUT, DELETE).</li>
<li><strong>XSS Prevention:</strong> Sanitize rich text inputs using libraries like Bleach to prevent malicious JavaScript execution.</li>
<li><strong>Session Fixation Protection:</strong> Regenerate session IDs on login.</li>
</ol>''',
                'author': created_users['sarah_tech'],
                'category': created_categories['Web Development'],
                'tags': [created_tags['Python'], created_tags['Flask'], created_tags['Security']],
                'days_ago': 3
            },
            {
                'title': 'Relational Database Design: One-to-Many and Many-to-Many in Practice',
                'summary': 'Learn how to model real-world relationships cleanly in SQLite and PostgreSQL using SQLAlchemy relationship attributes.',
                'content': '''<h2>Modeling Real-World Relationships</h2>
<p>Designing a relational schema requires careful consideration of entity cardinality. In this article, we examine common blogging schema patterns.</p>
<h3>One-to-Many: Authors and Articles</h3>
<p>A single user can author hundreds of posts, but each post has exactly one author. In SQLAlchemy, we specify a foreign key on the <code>posts</code> table referencing <code>users.id</code>.</p>
<h3>Many-to-Many: Posts and Tags</h3>
<p>A post can have multiple tags, and a tag can categorize thousands of posts. To achieve this without redundancy, we implement an association table with composite primary keys.</p>
<blockquote>"Proper normalization reduces data anomalies and keeps database queries blazing fast."</blockquote>''',
                'author': created_users['david_learner'],
                'category': created_categories['Database & SQL'],
                'tags': [created_tags['SQLAlchemy'], created_tags['Architecture'], created_tags['Tutorial']],
                'days_ago': 2
            },
            {
                'title': 'Crafting Responsive and Elegant UI with Bootstrap 5',
                'summary': 'Explore responsive flexbox grids, modern cards, and interactive components that bring modern web applications to life.',
                'content': '''<h2>Modern Web Interfaces Without Heavy Frontend Bundlers</h2>
<p>While heavy JavaScript frameworks have their place, server-rendered applications with Bootstrap 5 offer incredible performance, simplicity, and rapid development speed.</p>
<h3>Why Bootstrap 5 Stands Out</h3>
<ul>
<li><strong>No jQuery dependency:</strong> Vanilla JavaScript with high performance.</li>
<li><strong>CSS Grid & Flexbox:</strong> Intuitive layout mechanics for every screen size.</li>
<li><strong>Accessibility:</strong> Built-in ARIA attributes and focus management.</li>
</ul>
<p>Combining Bootstrap 5 with clean Jinja2 templates gives you a reactive-feeling platform with zero complex webpack builds.</p>''',
                'author': created_users['sarah_tech'],
                'category': created_categories['Web Development'],
                'tags': [created_tags['Bootstrap5'], created_tags['WebDev'], created_tags['Tutorial']],
                'days_ago': 1
            }
        ]

        created_posts = []
        for p_data in posts_data:
            post = Post(
                title=p_data['title'],
                slug=slugify(p_data['title']),
                summary=p_data['summary'],
                content=sanitize_html(p_data['content']),
                author=p_data['author'],
                category=p_data['category'],
                tags=p_data['tags'],
                created_at=datetime.now(timezone.utc) - timedelta(days=p_data['days_ago']),
                updated_at=datetime.now(timezone.utc) - timedelta(days=p_data['days_ago'])
            )
            db.session.add(post)
            created_posts.append(post)

        db.session.commit()
        print(f"Created {len(created_posts)} sample posts.")

        # 5. Create Sample Comments
        comments_data = [
            {
                'content': 'This is a fantastic explanation of the application factory pattern! It saved me so much time while configuring unit tests.',
                'author': created_users['david_learner'],
                'post': created_posts[0]
            },
            {
                'content': 'Great insights on Bleach and XSS prevention. Security is so often overlooked in tutorial projects.',
                'author': created_users['alex_dev'],
                'post': created_posts[1]
            },
            {
                'content': 'Clean and concise guide. Really helped me understand many-to-many association tables in SQLAlchemy.',
                'author': created_users['sarah_tech'],
                'post': created_posts[2]
            }
        ]

        for c_data in comments_data:
            comment = Comment(
                content=c_data['content'],
                author=c_data['author'],
                post=c_data['post'],
                created_at=datetime.now(timezone.utc) - timedelta(hours=12)
            )
            db.session.add(comment)

        db.session.commit()
        print(f"Created {len(comments_data)} sample comments.")
        print('Database successfully seeded with comprehensive sample data!')


@app.cli.command('init-db')
def init_db():
    create_tables()


@app.cli.command('seed-db')
def seed_db():
    populate_seed()


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'seed-db':
        populate_seed()
    elif len(sys.argv) > 1 and sys.argv[1] == 'init-db':
        create_tables()
    else:
        app.run(debug=True, host='127.0.0.1', port=5000)
