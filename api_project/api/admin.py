from django.contrib import admin
from .models import Book
from django.contrib.admin.sites import AlreadyRegistered

try:
    admin.site.register(Book)
except AlreadyRegistered:
    pass


