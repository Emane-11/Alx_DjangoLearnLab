from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Author
from .serializers import AuthorSerializer

@api_view(['GET'])
def author_list(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)


from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

"""
View Classes:
- BookListView: Lists all books (read-only).
- BookDetailView: Retrieves one book by ID (read-only).
- BookCreateView: Allows authenticated users to add books.
- BookUpdateView: Allows authenticated users to edit books.
- BookDeleteView: Allows authenticated users to remove books.

Permissions:
- Read operations: Public access.
- Write operations: Restricted to authenticated users.

Customizations:
- perform_create: Hook to customize how books are created.
"""

# List all books (read-only, open to everyone)
class BookListView(generics.ListAPIView):
    """
    GET: Retrieve a list of all books.
    Open to all users (authenticated or not).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# Retrieve single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve details of a single book by ID.
    Open to all users (authenticated or not).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# Create a new book (restricted to authenticated users)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Example: Automatically set author based on request user (if applicable)
        # serializer.save(author=self.request.user.author_profile)
        serializer.save()  # Keeping it generic for now


# Update an existing book (restricted to authenticated users)
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update details of an existing book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# Delete a book (restricted to authenticated users)
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Remove a book from the database.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


