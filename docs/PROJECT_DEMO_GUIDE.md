# DevScribe: Project Demonstration Guide
## Step-by-Step Evaluator & Mentor Walkthrough

This guide provides a structured, click-by-click testing sequence to demonstrate all 8 weeks of engineering deliverables in DevScribe.

---

## ⚡ Quick Start Checklist

1. **Activate Virtual Environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
2. **Seed Clean Test Data (if needed):**
   ```powershell
   python run.py seed-db
   ```
3. **Launch the Flask Server:**
   ```powershell
   python run.py
   ```
4. **Open in Browser:** `http://127.0.0.1:5000`

---

## 👥 Seeded Demo Accounts

| Role | Username | Email | Password |
|:---|:---|:---|:---|
| Primary Author | `alex_dev` | `alex@example.com` | `password123` |
| Secondary Author | `sarah_tech` | `sarah@example.com` | `password123` |
| Student / Reader | `david_learner` | `david@example.com` | `password123` |

---

## 🧭 Step-by-Step Feature Walkthrough

### Step 1: Explore the Homepage (Week 1 & Week 4)
1. Navigate to `http://127.0.0.1:5000/`.
2. Notice the **Hero Banner** with interactive shell preview and live statistics.
3. Observe the **Featured Story card** with category badge and estimated reading time.
4. Review the **Browse Topics strip** and the **Latest Publications grid**.
5. Test responsive behavior by resizing your browser window or toggling mobile device mode in Developer Tools (F12).

### Step 2: Test User Registration (Week 2)
1. In the navigation bar, click **"Get Started"** (or go to `/register`).
2. Try submitting with missing fields or mismatched passwords to verify client/server validation errors.
3. Register a new user:
   - Username: `test_engineer`
   - Email: `engineer@example.com`
   - Password: `password123`
   - Confirm Password: `password123`
4. Confirm successful registration flash alert and automatic redirection to the login page.

### Step 3: Test User Login & Dashboard (Week 2)
1. On the Login page (`/login`), click the button **"Login as alex_dev"** to test instant autofill.
2. Click **"Sign In"**.
3. Verify redirection to the **Author Dashboard** (`/dashboard`).
4. Review the three metrics:
   - Articles Published
   - Reader Comments Received
   - Comments Contributed
5. Review the article management table listing published stories with edit and delete options.

### Step 4: Create a New Post with Rich Text & Tags (Week 3)
1. In the dashboard or navbar, click **"Write Article"** (`/posts/create`).
2. Fill the form:
   - **Title:** `Building Scalable APIs with Flask 3`
   - **Summary:** `A practical walkthrough of REST API architecture.`
   - **Category:** Select `Python & Flask`.
   - **Tags:** `Python, Flask, API, Architecture`
   - **Content:** Use the **Quill.js toolbar** to add an H2 heading, bold text, a bullet list, and a code block.
3. Click **"Publish Article"**.
4. Confirm flash message and automatic redirection to the published story detail page.

### Step 5: Verify Detail Page, Reading Time & XSS Protection (Weeks 3 & 7)
1. On the published article page:
   - Notice the automatically calculated reading time (e.g. *2 min read*).
   - Check the author line with avatar and publication timestamp.
   - Verify that Quill rich text formatting rendered cleanly.
   - Note the tag pills at the bottom.
2. In `app/utils.py`, review the `sanitize_html()` implementation using Bleach to confirm XSS protection.

### Step 6: Test Post Update and Delete Authorization (Week 3)
1. On the article detail page, click **"Edit Story"** (or edit from dashboard).
2. Modify the title and update the tags. Click **"Save Changes"**.
3. Notice that changes persist immediately and the page shows `(Updated ...)`.
4. Return to the dashboard and test the **Delete Post** button:
   - Notice the Bootstrap modal prompt asking for confirmation.
   - Confirm deletion to verify the article is cleanly removed.

### Step 7: Test the Commenting System & Moderation (Week 5)
1. Navigate to any published article (e.g. *"Mastering Secure User Authentication"*).
2. Scroll to the **Discussions** section at the bottom.
3. Enter a comment: `This guide helped me understand password hashing!`
4. Click **"Post Comment"**.
5. Observe the comment appearing with your avatar, name, and relative timestamp.
6. Notice that the comment author can delete their comment, and the post author also has the trash icon to moderate comments on their post.

### Step 8: Test Search, Filtering, and Sorting (Week 6)
1. In the navigation bar search bar, type `Flask` and press Enter.
2. On the Search results page (`/search?q=Flask`):
   - Notice the query filter badge.
   - Click a category in the sidebar to filter simultaneously.
   - Change the sorting to **"Oldest"** and then **"Most Discussed"**.
3. Clear search and observe the empty state by searching for a nonsense term: `xyz999`.

### Step 9: Run Automated Tests (Week 7)
Open a terminal in the project directory and execute:
```powershell
python -m unittest discover -s tests -v
```
Verify that all 31 tests pass with:
```
Ran 31 tests in ...s
OK
```
