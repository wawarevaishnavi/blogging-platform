from urllib.parse import urlsplit
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User, Post, Comment
from app.forms import RegistrationForm, LoginForm, ProfileForm

auth_bp = Blueprint('auth', __name__)


def is_safe_redirect_url(target: str) -> bool:
    """Ensure redirect URL is local to prevent open-redirect vulnerabilities."""
    if not target:
        return False
    ref_url = urlsplit(request.host_url)
    test_url = urlsplit(target)
    return test_url.scheme in ('', 'http', 'https') and (test_url.netloc == '' or test_url.netloc == ref_url.netloc)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user account."""
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower()
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Authenticate and log in an existing user."""
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        credential = form.email_or_username.data.strip()
        # Look up by email or username
        user = User.query.filter(
            (User.email == credential.lower()) | (User.username == credential)
        ).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'Welcome back, {user.username}!', 'success')

            next_page = request.args.get('next')
            if next_page and is_safe_redirect_url(next_page):
                return redirect(next_page)
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid username/email or password. Please check your credentials.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """Log out the current authenticated user."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    """Authenticated user dashboard with article management and statistics."""
    page = request.args.get('page', 1, type=int)
    posts_pagination = Post.query.filter_by(user_id=current_user.id)\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)

    user_posts = posts_pagination.items
    total_posts = Post.query.filter_by(user_id=current_user.id).count()

    # Calculate total comments received across all author's posts
    post_ids = [p.id for p in Post.query.filter_by(user_id=current_user.id).all()]
    total_comments_received = Comment.query.filter(Comment.post_id.in_(post_ids)).count() if post_ids else 0
    total_comments_made = Comment.query.filter_by(user_id=current_user.id).count()

    stats = {
        'total_posts': total_posts,
        'total_comments_received': total_comments_received,
        'total_comments_made': total_comments_made
    }

    return render_template(
        'auth/dashboard.html',
        posts=user_posts,
        pagination=posts_pagination,
        stats=stats
    )


@auth_bp.route('/profile/<username>')
def user_profile(username):
    """Public profile view of an author and their published articles."""
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts_pagination = Post.query.filter_by(user_id=user.id)\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=6, error_out=False)

    return render_template(
        'auth/profile.html',
        author=user,
        posts=posts_pagination.items,
        pagination=posts_pagination
    )


@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit current user's profile information."""
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.bio = form.bio.data.strip()
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('auth.user_profile', username=current_user.username))
    elif request.method == 'GET':
        form.bio.data = current_user.bio

    return render_template('auth/edit_profile.html', form=form)
