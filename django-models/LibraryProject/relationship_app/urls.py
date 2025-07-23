from django.urls import path
from .views import list_books, RegisterView, CustomLogoutView, LibraryDetailView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('books/', list_books, name='list_books'),  # FBV
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # CBV

    # Auth URLs
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]

