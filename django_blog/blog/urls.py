from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="blog/logged_out.html"), name="logout"),
    path("profile/", views.profile_view, name="profile"),
]

# Post URLs
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),        # Create
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),  # Update
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),  # Delete
]
