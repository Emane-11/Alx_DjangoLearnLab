from django.shortcuts import render
from .models import Book
from django.contrib.auth import login


def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


from django.views.generic.detail import DetailView
from .models import Library

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

# Registration View
class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})

    def post(self, request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)  # Log the user in immediately after registration
        return redirect('list_books')  # Or any other success page
    return render(request, 'relationship_app/register.html', {'form': form})


from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

# Admin view
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

def is_admin(user):
    return user.userprofile.role == 'Admin'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian view
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

def is_librarian(user):
    return user.userprofile.role == 'Librarian'

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member view
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

def is_member(user):
    return user.userprofile.role == 'Member'

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')





