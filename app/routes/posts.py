import re
from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Post, Category, Tag, Comment
from app.forms import PostForm, CategoryForm, CommentForm
from app.utils import sanitize_html, slugify

posts_bp = Blueprint('posts', __name__)


def generate_unique_slug(model, title: str, current_id: int = None) -> str:
    """Generate a unique slug for a model, appending a counter if conflicts exist."""
    base_slug = slugify(title)
    if not base_slug:
        base_slug = 'untitled-post'
    slug = base_slug
    counter = 1

    while True:
        query = model.query.filter_by(slug=slug)
        if current_id:
            query = query.filter(model.id != current_id)
        if not query.first():
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1


def process_tags(tag_string: str) -> list:
    """Parse comma-separated tag string, retrieve or create Tag instances."""
    if not tag_string:
        return []
    raw_tags = [t.strip() for t in tag_string.split(',') if t.strip()]
    unique_names = {}
    for name in raw_tags:
        clean_name = name.lower()
        if clean_name not in unique_names:
            unique_names[clean_name] = name

    tag_objects = []
    for clean_name, original_name in unique_names.items():
        tag = Tag.query.filter_by(name=original_name).first()
        if not tag:
            # Check by slug
            tag_slug = slugify(original_name)
            tag = Tag.query.filter_by(slug=tag_slug).first()
        if not tag:
            tag = Tag(name=original_name, slug=slugify(original_name))
            db.session.add(tag)
        tag_objects.append(tag)
    return tag_objects


@posts_bp.route('/posts')
def all_posts():
    """Browse all published blog posts with sorting, filtering, and pagination."""
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort', 'newest').strip().lower()
    category_slug = request.args.get('category', '').strip()
    tag_slug = request.args.get('tag', '').strip()
    per_page = current_app.config.get('POSTS_PER_PAGE', 6)

    query = Post.query

    selected_category = None
    if category_slug:
        selected_category = Category.query.filter_by(slug=category_slug).first()
        if selected_category:
            query = query.filter(Post.category_id == selected_category.id)

    selected_tag = None
    if tag_slug:
        selected_tag = Tag.query.filter_by(slug=tag_slug).first()
        if selected_tag:
            query = query.filter(Post.tags.any(id=selected_tag.id))

    if sort_by == 'oldest':
        query = query.order_by(Post.created_at.asc())
    elif sort_by == 'popular':
        query = query.outerjoin(Comment).group_by(Post.id).order_by(db.func.count(Comment.id).desc())
    else:
        query = query.order_by(Post.created_at.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    categories = Category.query.all()
    popular_tags = Tag.query.limit(20).all()

    return render_template(
        'posts/all_posts.html',
        posts=pagination.items,
        pagination=pagination,
        selected_category=selected_category,
        selected_tag=selected_tag,
        sort_by=sort_by,
        categories=categories,
        popular_tags=popular_tags
    )


@posts_bp.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create a new blog post with rich text and category/tag tagging."""
    form = PostForm()
    # Populate categories
    categories = Category.query.order_by(Category.name.asc()).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

    if not categories:
        flash('Please create at least one category before publishing a post.', 'warning')
        return redirect(url_for('posts.create_category'))

    if form.validate_on_submit():
        sanitized_content = sanitize_html(form.content.data)
        slug = generate_unique_slug(Post, form.title.data)
        tags = process_tags(form.tags.data)

        post = Post(
            title=form.title.data.strip(),
            slug=slug,
            summary=form.summary.data.strip() if form.summary.data else None,
            content=sanitized_content,
            user_id=current_user.id,
            category_id=form.category_id.data,
            tags=tags
        )
        db.session.add(post)
        db.session.commit()

        flash('Your blog post has been published successfully!', 'success')
        return redirect(url_for('posts.post_detail', slug=post.slug))

    return render_template('posts/create_post.html', form=form, categories=categories)


@posts_bp.route('/posts/<slug>')
def post_detail(slug):
    """View an individual blog post, its comments, and author information."""
    post = Post.query.filter_by(slug=slug).first_or_404()
    comment_form = CommentForm()

    # Related posts in the same category
    related_posts = []
    if post.category_id:
        related_posts = Post.query.filter(
            Post.category_id == post.category_id,
            Post.id != post.id
        ).order_by(Post.created_at.desc()).limit(3).all()

    return render_template(
        'posts/post_detail.html',
        post=post,
        comment_form=comment_form,
        related_posts=related_posts
    )


@posts_bp.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Edit an existing blog post (restricted to post owner)."""
    post = Post.query.get_or_404(post_id)

    # Authorization verification
    if post.author != current_user:
        flash('You are not authorized to edit this post.', 'danger')
        abort(403)

    form = PostForm()
    categories = Category.query.order_by(Category.name.asc()).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        post.title = form.title.data.strip()
        # Regenerate slug if title changed
        post.slug = generate_unique_slug(Post, post.title, current_id=post.id)
        post.summary = form.summary.data.strip() if form.summary.data else None
        post.content = sanitize_html(form.content.data)
        post.category_id = form.category_id.data
        post.tags = process_tags(form.tags.data)
        post.updated_at = datetime.now(timezone.utc)

        db.session.commit()
        flash('Your blog post has been updated successfully!', 'success')
        return redirect(url_for('posts.post_detail', slug=post.slug))

    elif request.method == 'GET':
        form.title.data = post.title
        form.summary.data = post.summary
        form.category_id.data = post.category_id
        form.tags.data = ', '.join([t.name for t in post.tags])
        form.content.data = post.content

    return render_template('posts/edit_post.html', form=form, post=post, categories=categories)


@posts_bp.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a blog post (restricted to post owner)."""
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        flash('You are not authorized to delete this post.', 'danger')
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Blog post has been deleted successfully.', 'info')
    return redirect(url_for('auth.dashboard'))


@posts_bp.route('/categories')
def categories_list():
    """List all blog categories with article counts."""
    categories = Category.query.order_by(Category.name.asc()).all()
    return render_template('posts/categories.html', categories=categories)


@posts_bp.route('/category/<slug>')
def category_posts(slug):
    """Browse posts belonging to a specific category."""
    category = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE', 6)

    pagination = Post.query.filter_by(category_id=category.id)\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'posts/category_posts.html',
        category=category,
        posts=pagination.items,
        pagination=pagination
    )


@posts_bp.route('/category/create', methods=['GET', 'POST'])
@login_required
def create_category():
    """Create a new category for organizing blog posts."""
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data.strip(),
            description=form.description.data.strip() if form.description.data else None,
            slug=slugify(form.name.data.strip())
        )
        db.session.add(category)
        db.session.commit()
        flash(f'Category "{category.name}" created successfully!', 'success')
        return redirect(url_for('posts.categories_list'))

    return render_template('posts/create_category.html', form=form)


@posts_bp.route('/tag/<slug>')
def tag_posts(slug):
    """Browse posts tagged with a specific tag."""
    tag = Tag.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE', 6)

    pagination = Post.query.filter(Post.tags.any(id=tag.id))\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'posts/tag_posts.html',
        tag=tag,
        posts=pagination.items,
        pagination=pagination
    )
