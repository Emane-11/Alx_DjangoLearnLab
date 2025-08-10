"""
BookSerializer:
- Serializes all Book fields.
- Validates publication_year to ensure it's not in the future.

AuthorSerializer:
- Serializes author's name.
- Includes nested BookSerializer for all related books.
"""

from rest_framework import serializers
from datetime import datetime
from .models import Author, Book

# Serializes Book model with all fields
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    # Custom validation for publication_year
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# Serializes Author model with nested books
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  
    # 'books' is from the related_name in Book model

    class Meta:
        model = Author
        fields = ['name', 'books']
