from django.contrib import admin
from .models import Book

# Simple registration
# admin.site.register(Book)

# Enhanced registration
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Show these in list view
    list_filter = ('publication_year',)                     # Filter by year
    search_fields = ('title', 'author')                     # Search by title or author

