from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} by {self.author}"



from django.contrib import admin
from .models import Book  # Import your Book model

admin.site.register(Book)  # Register the Book model
