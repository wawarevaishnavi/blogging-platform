from flask import Blueprint, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Post, Comment
from app.forms import CommentForm
from app.utils import sanitize_html

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/posts/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    """Add a new comment to a blog post."""
    post = Post.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        clean_content = sanitize_html(form.content.data.strip())
        if not clean_content:
            flash('Comment cannot be empty or invalid.', 'danger')
            return redirect(url_for('posts.post_detail', slug=post.slug, _anchor='comments'))

        comment = Comment(
            content=clean_content,
            user_id=current_user.id,
            post_id=post.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Comment error: {error}', 'danger')

    return redirect(url_for('posts.post_detail', slug=post.slug, _anchor='comments'))


@comments_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """Delete a comment (allowed by the comment author or the post author)."""
    comment = Comment.query.get_or_404(comment_id)
    post_slug = comment.post.slug

    if comment.author != current_user and comment.post.author != current_user:
        flash('You are not authorized to delete this comment.', 'danger')
        abort(403)

    db.session.delete(comment)
    db.session.commit()
    flash('Comment has been deleted.', 'info')
    return redirect(url_for('posts.post_detail', slug=post_slug, _anchor='comments'))
