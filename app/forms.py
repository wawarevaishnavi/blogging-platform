from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError, Optional
from app.models import User, Category


class RegistrationForm(FlaskForm):
    """User registration form with strict validation."""
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required.'),
            Length(min=3, max=30, message='Username must be between 3 and 30 characters.'),
            Regexp(r'^[A-Za-z0-9_]+$', message='Username must contain only letters, numbers, and underscores.')
        ],
        render_kw={'placeholder': 'Choose a unique username'}
    )
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(message='Email address is required.'),
            Email(message='Please provide a valid email address.'),
            Length(max=120)
        ],
        render_kw={'placeholder': 'you@example.com'}
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required.'),
            Length(min=6, max=64, message='Password must be at least 6 characters.')
        ],
        render_kw={'placeholder': 'Minimum 6 characters'}
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message='Please confirm your password.'),
            EqualTo('password', message='Passwords must match.')
        ],
        render_kw={'placeholder': 'Re-enter your password'}
    )
    submit = SubmitField('Create Account')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data.strip()).first():
            raise ValidationError('This username is already taken. Please choose another.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.strip().lower()).first():
            raise ValidationError('An account with this email already exists.')


class LoginForm(FlaskForm):
    """User login form supporting either email or username."""
    email_or_username = StringField(
        'Email or Username',
        validators=[DataRequired(message='Please enter your email or username.')],
        render_kw={'placeholder': 'Enter email or username'}
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message='Please enter your password.')],
        render_kw={'placeholder': 'Enter password'}
    )
    remember_me = BooleanField('Keep me signed in')
    submit = SubmitField('Sign In')


class PostForm(FlaskForm):
    """Form for creating and editing blog posts."""
    title = StringField(
        'Post Title',
        validators=[
            DataRequired(message='Post title is required.'),
            Length(min=5, max=200, message='Title must be between 5 and 200 characters.')
        ],
        render_kw={'placeholder': 'Give your post an engaging title...'}
    )
    summary = StringField(
        'Short Summary / Subtitle',
        validators=[Length(max=350, message='Summary cannot exceed 350 characters.')],
        render_kw={'placeholder': 'Brief teaser that appears on post cards (optional)'}
    )
    category_id = SelectField(
        'Category',
        coerce=int,
        validators=[DataRequired(message='Please select a category.')]
    )
    tags = StringField(
        'Tags',
        validators=[Optional(), Length(max=200)],
        render_kw={'placeholder': 'e.g. python, flask, tutorial (comma separated)'}
    )
    content = TextAreaField(
        'Content',
        validators=[DataRequired(message='Post content cannot be empty.')],
        render_kw={'id': 'editor-textarea'}
    )
    submit = SubmitField('Publish Post')


class CategoryForm(FlaskForm):
    """Form for adding a new blog category."""
    name = StringField(
        'Category Name',
        validators=[
            DataRequired(message='Category name is required.'),
            Length(min=2, max=64, message='Category name must be between 2 and 64 characters.')
        ],
        render_kw={'placeholder': 'e.g. Web Development, AI & ML, Architecture'}
    )
    description = TextAreaField(
        'Description',
        validators=[Optional(), Length(max=255)],
        render_kw={'placeholder': 'Briefly describe what articles belong in this category.'}
    )
    submit = SubmitField('Save Category')

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data.strip()).first():
            raise ValidationError('A category with this name already exists.')


class CommentForm(FlaskForm):
    """Form for submitting a comment on a blog post."""
    content = TextAreaField(
        'Leave a Comment',
        validators=[
            DataRequired(message='Comment cannot be empty.'),
            Length(min=3, max=1000, message='Comment must be between 3 and 1000 characters.')
        ],
        render_kw={'placeholder': 'Share your thoughts or feedback on this article...', 'rows': 3}
    )
    submit = SubmitField('Post Comment')


class ProfileForm(FlaskForm):
    """Form for updating user profile bio."""
    bio = TextAreaField(
        'About You',
        validators=[Optional(), Length(max=500, message='Bio cannot exceed 500 characters.')],
        render_kw={'placeholder': 'Tell readers about yourself, your background, or your interests...', 'rows': 4}
    )
    submit = SubmitField('Update Profile')
