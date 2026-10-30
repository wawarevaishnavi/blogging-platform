# DevScribe: Internship Screenshots Checklist
## Visual Evidence Guide for Final Submission

Use this checklist to capture high-resolution screenshots (PNG, 1920x1080) for your final internship presentation slides and project report.

---

## 📸 Checklist of Required Screenshots

| # | Screenshot Identifier | Route / View | What to Show / Focus On |
|:---|:---|:---|:---|
| **01** | `01_homepage_hero.png` | `/` | Hero banner with gradient text, interactive terminal preview, and stats. |
| **02** | `02_homepage_featured.png` | `/` | Featured story showcase card with category badge, reading time, and author avatar. |
| **03** | `03_homepage_posts_grid.png` | `/` | Responsive grid of latest publications with tag pills and comment counters. |
| **04** | `04_register_page.png` | `/register` | Registration form card with username, email, password, and validation hints. |
| **05** | `05_register_validation.png` | `/register` | Form showing field validation error messages (e.g. duplicate username/email). |
| **06** | `06_login_page.png` | `/login` | Modern login portal with the one-click demo credentials autofill pills. |
| **07** | `07_author_dashboard.png` | `/dashboard` | Author dashboard showing metric statistics cards (Total Posts, Comments Received). |
| **08** | `08_dashboard_table.png` | `/dashboard` | Articles management table with Category badges, comments count, and action buttons. |
| **09** | `09_create_post_quill.png` | `/posts/create` | Article authoring interface with Quill.js rich text editor toolbar active. |
| **10** | `10_post_detail_view.png` | `/posts/<slug>` | Full published article view with sanitized rich text, headings, and code blocks. |
| **11** | `11_author_bio_box.png` | `/posts/<slug>` | Author biography card at bottom of article with avatar and credential details. |
| **12** | `12_comments_section.png` | `/posts/<slug>#comments` | Active discussion thread showing comments with avatars and relative timestamps. |
| **13** | `13_comment_guest_prompt.png` | `/posts/<slug>#comments` | Guest prompt inviting unauthenticated users to sign in to comment. |
| **14** | `14_delete_modal.png` | `/dashboard` or `/posts/<slug>` | Bootstrap modal dialog confirming deletion before executing database delete. |
| **15** | `15_search_results.png` | `/search?q=Flask` | Search results showing active filter badges, query count, and sort controls. |
| **16** | `16_search_empty_state.png` | `/search?q=xyz` | Illustrated empty state card when search query finds no matching records. |
| **17** | `17_categories_grid.png` | `/categories` | Categories gallery cards showing topic descriptions and live post counts. |
| **18** | `18_author_profile.png` | `/profile/<username>` | Public author profile page displaying bio, member date, and published articles. |
| **19** | `19_mobile_responsive.png` | Mobile View (375px) | Responsive mobile view showing collapsible navigation and stacked cards. |
| **20** | `20_automated_tests_pass.png` | Terminal | Command prompt showing `python -m unittest discover -s tests -v` passing all 31 tests. |

---

## 💡 Screenshot Capture Best Practices

1. **Browser Appearance:**
   - Use Google Chrome or Microsoft Edge at 100% or 110% zoom.
   - Hide the browser bookmarks bar (Ctrl + Shift + B) for clean presentation.
2. **Data Consistency:**
   - Run `python run.py seed-db` beforehand so that posts have realistic dates, tags, and comments.
3. **Naming Convention:**
   - Save screenshots directly into a `screenshots/` directory using the naming identifiers listed above.
