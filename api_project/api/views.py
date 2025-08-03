from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

''' ⬆️ This single class handles:

GET /books_all/ → list

GET /books_all/<id>/ → retrieve

POST /books_all/ → create

PUT /books_all/<id>/ → update

DELETE /books_all/<id>/ → destroy'''

