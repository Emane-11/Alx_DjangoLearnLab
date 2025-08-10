"""
Author model:
- Stores author names.
- Related to Book via a one-to-many relationship.

Book model:
- Stores book titles, publication years.
- Links to Author via ForeignKey.
- related_name='books' allows reverse lookup.
"""

from django.db import models
from datetime import datetime

class Author(models.Model):
    name = models.CharField(max_length=255)  

    def __str__(self):
        return self.name



class Book(models.Model):
    title = models.CharField(max_length=255)  
    publication_year = models.IntegerField()  
    author = models.ForeignKey(
        Author,
        related_name='books',  # Allows reverse access: author.books.all()
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

