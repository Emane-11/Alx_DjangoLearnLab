from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description']

# Add this if the task expects a separate form class (e.g., for custom input or testing CSRF)
class ExampleForm(forms.Form):
    title = forms.CharField(max_length=200)
    author = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        # Add any custom validation here
        return title
