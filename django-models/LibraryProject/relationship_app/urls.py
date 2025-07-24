from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .views import list_books, register, CustomLogoutView, LibraryDetailView
from .views import admin_view, librarian_view, member_view

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

urlpatterns = [
    path('books/', views.list_books, name='list_books'),  # FBV
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # CBV

     # Auth
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'), 
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/', views.register, name='register'),

    # Role-specific views
    path('admin-dashboard/', admin_view, name='admin_view'),
    path('librarian-dashboard/', librarian_view, name='librarian_view'),
    path('member-dashboard/', member_view, name='member_view'),
]


