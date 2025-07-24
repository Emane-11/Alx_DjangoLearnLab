from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

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
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'), 
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/', views.register, name='register'),
]


