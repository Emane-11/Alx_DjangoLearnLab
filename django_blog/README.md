Django Blog Project Documentation

Project Overview

This Django blog project allows users to:

Register, log in, and manage their profiles

Create, read, update, and delete blog posts

Comment on posts

Tag posts for easy categorization

Search for posts using keywords or tags

The project is designed to demonstrate Django fundamentals, including models, forms, views, templates, and user authentication.

1. User Authentication
Features

Registration: Users can create an account with a username, email, and password.

Login/Logout: Authenticated users can log in and log out securely.

Profile Management: Users can view and update their profile information.

Usage

Register: Navigate to /register/ and fill out the registration form.

Login: Navigate to /login/ and enter your credentials.

Logout: Click the logout link or navigate to /logout/.

Edit Profile: Navigate to /profile/ to update your email or other optional fields.

Security

Passwords are hashed using Django’s built-in algorithms.

All forms include CSRF protection.

2. Blog Post Management (CRUD)
Features

Create Post: Authenticated users can create posts with a title, content, and optional tags.

Read Post: Any visitor can view all posts or a single post.

Update Post: Only the author can edit their post.

Delete Post: Only the author can delete their post.

Usage

Create Post: Navigate to /posts/new/.

View Posts: Navigate to /posts/ to see all posts.

View Single Post: Click a post title or navigate to /posts/<id>/.

Edit Post: Navigate to /posts/<id>/edit/.

Delete Post: Navigate to /posts/<id>/delete/.

Permissions

LoginRequiredMixin ensures only logged-in users can create posts.

UserPassesTestMixin ensures only the post author can edit or delete.

3. Comment Functionality
Features

Users can comment on blog posts.

Comment authors can edit or delete their own comments.

Usage

Add Comment: On a post detail page, click “Add Comment” and submit your text.

Edit/Delete Comment: Authors can edit or delete comments using the links next to their comment.

Permissions

Only logged-in users can add comments.

Only the comment author can edit or delete their comment.

4. Tagging System
Features

Posts can be assigned multiple tags for categorization.

Tags are displayed on the post detail page and are clickable to filter posts.

Usage

Add Tags: When creating or editing a post, enter tag names separated by commas.

View Posts by Tag: Click a tag to see all posts with that tag.
Example URL: /tags/django/

5. Search Functionality
Features

Users can search posts by title, content, or tags.

Search results display posts that match the query.

Usage

Enter a keyword or tag in the search bar and submit.

Example URL: /search/?q=django

6. Project Structure
django_blog/
├─ blog/
│  ├─ migrations/
│  ├─ templates/blog/
│  │  ├─ post_list.html
│  │  ├─ post_detail.html
│  │  ├─ post_form.html
│  │  ├─ post_confirm_delete.html
│  │  ├─ add_comment.html
│  │  ├─ comment_form.html
│  │  ├─ comment_confirm_delete.html
│  │  ├─ posts_by_tag.html
│  │  └─ post_search.html
│  ├─ forms.py
│  ├─ models.py
│  ├─ urls.py
│  └─ views.py
├─ django_blog/
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ manage.py
└─ requirements.txt

7. Setup Instructions

Clone the repository:

git clone <repo_url>
cd django_blog


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py migrate


Create a superuser (optional):

python manage.py createsuperuser


Run the development server:

python manage.py runserver


Visit the site: http://127.0.0.1:8000/

8. Notes

Ensure user authentication is working before adding posts or comments.

Tags require django-taggit.

Search supports queries on title, content, and tags.