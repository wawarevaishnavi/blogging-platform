# DevScribe: Final Project Completion Report
## DIY Internship Program — Full-Stack Python Flask Track (Weeks 1 - 8)

- **Project Title:** Blogging Platform with Flask ("DevScribe")
- **Author / Intern:** Full-Stack Engineering Intern
- **Technology Stack:** Python 3.14, Flask 3.1, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Bootstrap 5.3, Quill.js, Bleach, SQLite
- **Test Status:** 31 / 31 Tests Passing (100% Success Rate)
- **Deployment Status:** Ready for Production WSGI Deployment

---

## 1. Executive Summary

The **DevScribe Blogging Platform** is a full-stack, secure, modular web application engineered to satisfy all learning outcomes and technical deliverables across the 8-week DIY Internship curriculum.

Starting from an empty repository, the application was engineered using the Flask Application Factory pattern, normalized relational database models, cryptographic authentication, WYSIWYG rich-text editing, server-side XSS defense, real-time search, multi-faceted filtering, and discussion threads. Every backend endpoint is directly wired to interactive frontend templates styled with Bootstrap 5.

---

## 2. Week-Wise Milestone Completion Matrix

| Week | Milestone | Planned Objectives | Implemented Deliverables | Status |
|:---:|:---|:---|:---|:---:|
| **Week 1** | Flask Setup & Structure | Project structure, SQLite config, base templates, homepage, navbar/footer. | App factory (`create_app`), `config.py`, `extensions.py`, base Jinja2 layouts, responsive navbar and footer. | **Completed** |
| **Week 2** | User Authentication | Registration, login, logout, password hashing, Flask-Login, dashboard. | Werkzeug hashing (`scrypt`), Flask-Login user loader, protected routes, author dashboard with metric cards. | **Completed** |
| **Week 3** | Blog Post CRUD & Rich Text | Post, Category, Tag models; WTForms; CRUD operations; Quill.js; Bleach. | Full CRUD endpoints, slug generator, Quill editor integration, Bleach HTML sanitization, M:N tag associations. | **Completed** |
| **Week 4** | Frontend & Navigation | 10 modern pages, responsive Bootstrap 5 design, typography, card layouts. | Complete template suite: Home, Search, All Posts, Detail, Create, Edit, Categories, Profile, Dashboard, 403, 404, 500. | **Completed** |
| **Week 5** | Commenting System | Comment model, relationships, discussion thread, owner moderation. | `Comment` model, comment form with validation, relative timestamps, author moderation deletion. | **Completed** |
| **Week 6** | Search & Filtering | Keyword search by title/content, category/tag filters, sorting, pagination. | SQL `ILIKE` search, multi-criteria filtering, sorting by newest/oldest/popular, pagination controls. | **Completed** |
| **Week 7** | Testing & Deployment | 15 test criteria, requirements.txt, .env.example, README, seed CLI command. | 31 automated unit/integration tests with zero failures, CLI seeding command (`run.py seed-db`), deployment config. | **Completed** |
| **Week 8** | Presentation & Evaluation | Video script, demonstration sequence, screenshots checklist, completion report. | Complete 10-minute video presentation script, demo guide, screenshot capture checklist, and final report. | **Completed** |

---

## 3. Database Schema & Architecture

The database is built on **SQLite** using **SQLAlchemy ORM** with strict foreign keys and cascading relationships.

### Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    USER ||--o{ POST : "authors (1:N)"
    USER ||--o{ COMMENT : "writes (1:N)"
    CATEGORY ||--o{ POST : "classifies (1:N)"
    POST ||--o{ COMMENT : "contains (1:N)"
    POST }|--|{ TAG : "tagged_with (M:N via post_tags)"

    USER {
        int id PK
        string username UK
        string email UK
        string password_hash
        string bio
        datetime created_at
    }

    POST {
        int id PK
        string title
        string slug UK
        string summary
        text content
        datetime created_at
        datetime updated_at
        int user_id FK
        int category_id FK
    }

    CATEGORY {
        int id PK
        string name UK
        string slug UK
        string description
    }

    TAG {
        int id PK
        string name UK
        string slug UK
    }

    POST_TAGS {
        int post_id PK, FK
        int tag_id PK, FK
    }

    COMMENT {
        int id PK
        text content
        datetime created_at
        int user_id FK
        int post_id FK
    }
```

---

## 4. Security Architecture & Threat Mitigation

| Threat Vector | Mitigation Strategy | Implementation Details |
|:---|:---|:---|
| **Cross-Site Scripting (XSS)** | Pure server-side HTML sanitization | User content authored in Quill is filtered through **Bleach** (`app/utils.py`). Scripts, event handlers (`onerror`, `onclick`), and unsafe iframes are stripped. |
| **Cross-Site Request Forgery (CSRF)** | Synchronized Cryptographic Tokens | **Flask-WTF** CSRFProtect enforces unique secret tokens on all state-altering requests (POST/DELETE). |
| **Credential Compromise** | Cryptographic One-Way Hashing | Passwords are never stored in plain text. Salted hashes are generated using **Werkzeug** (`generate_password_hash` with `scrypt`). |
| **Unauthorized Data Modification** | Strict Ownership Verification | All update and delete routes verify `resource.author == current_user` before processing, returning `403 Forbidden` on unauthorized access. |
| **Open Redirect Vulnerability** | Host Validation | Login redirection checks target URLs via `is_safe_redirect_url()`, rejecting external phishing destinations. |
| **SQL Injection** | Parameterized Queries | SQLAlchemy declarative queries utilize bound parameters, eliminating raw SQL concatenation vulnerabilities. |

---

## 5. Automated Test Suite Results

The automated test suite was executed against an in-memory SQLite database using `unittest`.

```
Ran 31 tests in 9.095s
OK (All 31 tests passed with 0 errors and 0 failures)
```

### Breakdown of Test Cases:

| Test Module | Test Case Name | Objective Verified | Result |
|:---|:---|:---|:---:|
| `test_auth.py` | `test_user_password_hashing` | Werkzeug salted hash generation & verification | **PASS** |
| `test_auth.py` | `test_user_registration_success` | Valid registration workflow | **PASS** |
| `test_auth.py` | `test_registration_duplicate_username` | Duplicate username rejection | **PASS** |
| `test_auth.py` | `test_registration_duplicate_email` | Duplicate email rejection | **PASS** |
| `test_auth.py` | `test_registration_password_mismatch` | Password confirmation validation | **PASS** |
| `test_auth.py` | `test_login_and_logout` | Authentication session lifecycle | **PASS** |
| `test_auth.py` | `test_login_invalid_credentials` | Incorrect credential handling | **PASS** |
| `test_auth.py` | `test_protected_routes_require_login` | Unauthenticated redirect to login | **PASS** |
| `test_posts.py` | `test_create_post_success` | Post creation with category & tags | **PASS** |
| `test_posts.py` | `test_create_post_unauthenticated_redirects`| Route access protection | **PASS** |
| `test_posts.py` | `test_read_posts_and_detail` | Catalog and slug-based detail views | **PASS** |
| `test_posts.py` | `test_update_post_by_owner` | Owner post update capability | **PASS** |
| `test_posts.py` | `test_update_post_unauthorized_user_forbidden` | Non-owner edit blocked (403) | **PASS** |
| `test_posts.py` | `test_delete_post_by_owner` | Owner post deletion | **PASS** |
| `test_posts.py` | `test_delete_post_unauthorized_user_forbidden` | Non-owner delete blocked (403) | **PASS** |
| `test_comments.py` | `test_add_comment_success` | Authenticated comment submission | **PASS** |
| `test_comments.py` | `test_add_comment_unauthenticated_redirects` | Guest comment prompt redirection | **PASS** |
| `test_comments.py` | `test_delete_comment_by_comment_author` | Commenter deletion permission | **PASS** |
| `test_comments.py` | `test_delete_comment_by_post_author` | Post author moderation permission | **PASS** |
| `test_comments.py` | `test_delete_comment_unauthorized_forbidden` | Third-party deletion blocked (403) | **PASS** |
| `test_search_filter.py` | `test_search_by_title` | Title keyword search query | **PASS** |
| `test_search_filter.py` | `test_search_by_content` | Body keyword search query | **PASS** |
| `test_search_filter.py` | `test_filter_by_category` | Category slug filter | **PASS** |
| `test_search_filter.py` | `test_filter_by_tag` | Tag slug filter | **PASS** |
| `test_search_filter.py` | `test_sort_newest_vs_oldest` | Ascending and descending date sorting | **PASS** |
| `test_search_filter.py` | `test_empty_search_results` | Empty state handling | **PASS** |
| `test_security.py` | `test_xss_script_tags_stripped` | Bleach `<script>` tag stripping | **PASS** |
| `test_security.py` | `test_xss_onerror_attributes_stripped` | Inline event handler neutralization | **PASS** |
| `test_security.py` | `test_safe_rich_text_preserved` | Safe HTML preservation | **PASS** |
| `test_security.py` | `test_open_redirect_protection` | Phishing redirect blocking | **PASS** |
| `test_security.py` | `test_404_error_page` | Custom 404 error handler | **PASS** |

---

## 6. Final Evaluation Sign-Off

- [x] All 8 Weeks completed in strict sequential order.
- [x] Application Factory pattern implemented (`create_app`).
- [x] User registration, login, logout, and password hashing verified.
- [x] Full CRUD operations for Posts, Categories, and Tags tested.
- [x] Quill.js rich text editor integrated and tested.
- [x] Server-side Bleach HTML sanitization operational.
- [x] Commenting system with author moderation active.
- [x] Search, category filtering, tag filtering, sorting, and pagination functioning.
- [x] Responsive, modern UI designed with Bootstrap 5 and custom CSS.
- [x] Automated test suite executed with 31/31 passing tests.
- [x] Project presentation video script and demo documentation prepared.
- [x] Ready for final internship grading and presentation.
