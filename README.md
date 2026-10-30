# DevScribe: Complete Full-Stack Blogging Platform with Python Flask
## DIY Internship Project — Week 1 to Week 8 Capstone

DevScribe is an enterprise-grade, secure, responsive, full-stack blogging web application built with **Python**, **Flask 3.x**, **Flask-SQLAlchemy**, **Flask-Login**, **Flask-WTF**, **Bootstrap 5**, and **SQLite**.

Designed and executed as an 8-week software engineering internship capstone, this platform includes role-based CRUD functionality, password hashing, session management, rich text WYSIWYG editing with Quill.js, robust HTML sanitization with Bleach, multi-term keyword search, dynamic category and tag filtering, user discussion threads, and an automated test suite.

---

## 🌟 Key Features

### 1. User Authentication & Authorization (Weeks 1 & 2)
- **User Registration & Validation:** Unique username (alphanumeric + underscores), email validation, and password strength checks.
- **Cryptographic Security:** Passwords salted and hashed with Werkzeug (`scrypt`/`PBKDF2`).
- **Session Management:** Built on Flask-Login with `remember_me` persistence and secure session fixation protection.
- **Role & Ownership Guards:** Strictly prohibits unauthorized users from modifying or deleting posts or comments they do not own.

### 2. Complete Blog Post CRUD & Rich Text Editing (Weeks 3 & 4)
- **Create:** Publish rich technical articles with title, subtitle summary, category selection, comma-separated tags, and rich text formatting.
- **Read:** Individual article reading view with estimated reading time, author card, relative dates, category badges, tag pills, and related posts.
- **Update:** Full inline editing with pre-filled content, re-slugification, and automatic `updated_at` tracking.
- **Delete:** Modal-confirmed deletion with cascading cleanup of associated comments.
- **Quill.js Rich Text Editor:** Headings (H2-H4), bold, italic, underline, strike, ordered/bullet lists, blockquotes, inline and block code formatting, links.
- **XSS Sanitization:** All submitted HTML is scrubbed server-side via `bleach` to eliminate malicious scripts, iframes, and `onerror` handlers.

### 3. Commenting & Discussion System (Week 5)
- Logged-in users can participate in discussions on any article.
- Non-authenticated visitors see contextual login prompts.
- Dual-moderation permissions: Comments can be deleted by either the comment author or the article author.

### 4. Search, Filtering, and Pagination (Week 6)
- **Keyword Search:** SQL `ILIKE` searching across article titles, summaries, and contents.
- **Category & Tag Filters:** Filter by specific topic or tag pills with active filter removal chips.
- **Sorting Options:** Sort results by *Newest*, *Oldest*, or *Most Discussed*.
- **Pagination:** Clean Bootstrap pagination controls preserving query parameters.

### 5. Robust Automated Testing Suite (Week 7)
- **31 Unit & Integration Tests** covering Authentication, CRUD, Ownership Authorization, Comments, Search & Filter, and XSS Sanitization.
- Zero failures, 100% passing test execution.

---

## 🏗️ Project Architecture

```
blogging_platform/
├── app/
│   ├── __init__.py           # Application Factory pattern (create_app)
│   ├── config.py             # Development, Testing, Production configurations
│   ├── extensions.py         # SQLAlchemy, LoginManager, Migrate, CSRFProtect
│   ├── models.py             # User, Post, Category, Tag, Comment models
│   ├── forms.py              # Flask-WTF forms with custom validators
│   ├── utils.py              # Bleach HTML sanitizer, slugifier, reading time
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py           # Home, Search, About routes
│   │   ├── auth.py           # Register, Login, Logout, Dashboard, Profile routes
│   │   ├── posts.py          # Post CRUD, Categories, Tags routes
│   │   └── comments.py       # Add and Delete comment routes
│   ├── static/
│   │   ├── css/style.css     # Custom modern design system
│   │   └── js/main.js        # Quill editor integration, demo autofill, modals
│   └── templates/
│       ├── base.html         # Base layout with Bootstrap 5 & Quill CDN
│       ├── components/       # Reusable navbar, footer, alert banners
│       ├── main/             # index.html, search.html, about.html
│       ├── auth/             # register.html, login.html, dashboard.html, profile.html
│       ├── posts/            # all_posts, post_detail, create_post, edit_post, categories
│       └── errors/           # 403.html, 404.html, 500.html
├── instance/
│   └── blog.db               # SQLite database
├── tests/
│   ├── __init__.py
│   ├── test_auth.py          # Registration, login, password hashing tests
│   ├── test_posts.py         # CRUD operations and authorization tests
│   ├── test_comments.py      # Commenting and moderation tests
│   ├── test_search_filter.py # Search, category, tag, and sort tests
│   └── test_security.py      # XSS sanitization, open redirect, error handler tests
├── docs/
│   ├── INTERNSHIP_VIDEO_SCRIPT.md # Week 8: 10-minute video presentation script
│   ├── PROJECT_DEMO_GUIDE.md      # Step-by-step demonstration walkthrough
│   ├── SCREENSHOTS_CHECKLIST.md   # Screenshot capture guide for documentation
│   └── FINAL_COMPLETION_REPORT.md # Official internship submission report
├── .env.example              # Template environment variables
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
└── run.py                    # Application entry point & CLI commands
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (tested with Python 3.14)
- Git

### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone https://github.com/your-username/blogging-platform-flask.git
cd blogging-platform-flask

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Initialize & Seed Sample Database
Populate realistic sample categories, users, technical articles, tags, and comments:
```bash
python run.py seed-db
```
*Seeded Demo Accounts:*
- Username: `alex_dev` | Password: `password123`
- Username: `sarah_tech` | Password: `password123`
- Username: `david_learner` | Password: `password123`

### 4. Run Development Server
```bash
python run.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 🧪 Running Automated Tests
Run the comprehensive test suite (31 tests):
```bash
python -m unittest discover -s tests -v
```

---

## 🛡️ Security Best Practices Implemented
1. **CSRF Protection:** Synchronized tokens across all POST/DELETE requests via Flask-WTF.
2. **XSS Sanitization:** Pure HTML sanitization using `bleach.clean` and `linkify`. Scripts and arbitrary attributes are stripped before storage.
3. **Password Security:** Salted hashes generated via `werkzeug.security.generate_password_hash`.
4. **Owner Verification:** Strict ownership checks before any modification or deletion.
5. **Open Redirect Defense:** URL host validation on `?next=` parameters prevents redirection to malicious external domains.

---

## 📄 License
This project is developed for the 8-Week DIY Internship Program. Free for educational and non-commercial demonstration.
