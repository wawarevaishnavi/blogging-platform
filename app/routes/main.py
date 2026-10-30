from flask import Blueprint, render_template, request, current_app
from sqlalchemy import or_
from app.models import Post, Category, Tag, User, Comment
from app.extensions import db

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Homepage showcasing featured posts, categories, stats, and recent stories."""
    # Fetch recent posts
    all_recent = Post.query.order_by(Post.created_at.desc()).limit(7).all()
    featured_post = all_recent[0] if all_recent else None
    recent_posts = all_recent[1:7] if len(all_recent) > 1 else []

    # Categories and popular tags
    categories = Category.query.all()
    tags = Tag.query.limit(15).all()

    # Community statistics
    stats = {
        'total_posts': Post.query.count(),
        'total_authors': User.query.count(),
        'total_comments': Comment.query.count(),
        'total_categories': Category.query.count()
    }

    return render_template(
        'main/index.html',
        featured_post=featured_post,
        recent_posts=recent_posts,
        categories=categories,
        tags=tags,
        stats=stats
    )


@main_bp.route('/search')
def search():
    """Search and filtering endpoint for posts by title and content."""
    query = request.args.get('q', '').strip()
    category_slug = request.args.get('category', '').strip()
    tag_slug = request.args.get('tag', '').strip()
    sort_by = request.args.get('sort', 'newest').strip().lower()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE', 6)

    # Base query
    posts_query = Post.query

    # Search filter by title or content
    if query:
        search_filter = or_(
            Post.title.ilike(f'%{query}%'),
            Post.content.ilike(f'%{query}%'),
            Post.summary.ilike(f'%{query}%')
        )
        posts_query = posts_query.filter(search_filter)

    # Filter by category
    selected_category = None
    if category_slug:
        selected_category = Category.query.filter_by(slug=category_slug).first()
        if selected_category:
            posts_query = posts_query.filter(Post.category_id == selected_category.id)

    # Filter by tag
    selected_tag = None
    if tag_slug:
        selected_tag = Tag.query.filter_by(slug=tag_slug).first()
        if selected_tag:
            posts_query = posts_query.filter(Post.tags.any(id=selected_tag.id))

    # Sorting
    if sort_by == 'oldest':
        posts_query = posts_query.order_by(Post.created_at.asc())
    elif sort_by == 'popular':
        # Sort by comments count descending
        posts_query = posts_query.outerjoin(Comment).group_by(Post.id).order_by(db.func.count(Comment.id).desc())
    else:  # newest default
        posts_query = posts_query.order_by(Post.created_at.desc())

    # Pagination
    pagination = posts_query.paginate(page=page, per_page=per_page, error_out=False)
    posts = pagination.items

    categories = Category.query.all()
    popular_tags = Tag.query.limit(20).all()

    return render_template(
        'main/search.html',
        posts=posts,
        pagination=pagination,
        query=query,
        selected_category=selected_category,
        selected_tag=selected_tag,
        sort_by=sort_by,
        categories=categories,
        popular_tags=popular_tags
    )


@main_bp.route('/about')
def about():
    """About the internship project, architecture, and technology stack."""
    return render_template('main/about.html')
