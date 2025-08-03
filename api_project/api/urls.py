from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Basic list endpoint
    path('books/', BookList.as_view(), name='book-list'),

    # CRUD routes from the router
    path('', include(router.urls)),
]

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns += [
    path('token/', obtain_auth_token, name='api-token'),
]