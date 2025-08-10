from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITestCase(APITestCase):
    """Test suite for Book API endpoints."""

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        # Create test authors
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        # Create test books
        self.book1 = Book.objects.create(
            title="Book One",
            publication_year=2020,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Book Two",
            publication_year=2022,
            author=self.author2
        )

        # Endpoints
        self.list_url = reverse("book-list")
        self.create_url = reverse("book-create")
        self.detail_url = reverse("book-detail", kwargs={"pk": self.book1.pk})
        self.update_url = reverse("book-update", kwargs={"pk": self.book1.pk})
        self.delete_url = reverse("book-delete", kwargs={"pk": self.book1.pk})

    # --- READ TESTS ---
    def test_list_books(self):
        """Ensure we can retrieve the book list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_retrieve_single_book(self):
        """Ensure we can retrieve a single book by ID."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    # --- CREATE TEST ---
    def test_create_book_authenticated(self):
        """Ensure authenticated users can create books."""
        self.client.login(username="testuser", password="testpass123")
        data = {
            "title": "New Book",
            "publication_year": 2023,
            "author": self.author1.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        """Ensure unauthenticated users cannot create books."""
        data = {
            "title": "Fail Book",
            "publication_year": 2023,
            "author": self.author1.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- UPDATE TEST ---
    def test_update_book_authenticated(self):
        """Ensure authenticated users can update books."""
        self.client.login(username="testuser", password="testpass123")
        data = {"title": "Updated Title"}
        response = self.client.patch(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_update_book_unauthenticated(self):
        """Ensure unauthenticated users cannot update books."""
        data = {"title": "Hacker Update"}
        response = self.client.patch(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- DELETE TEST ---
    def test_delete_book_authenticated(self):
        """Ensure authenticated users can delete books."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_delete_book_unauthenticated(self):
        """Ensure unauthenticated users cannot delete books."""
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- FILTERING / SEARCHING / ORDERING ---
    def test_filter_books_by_author(self):
        """Ensure filtering by author works."""
        response = self.client.get(f"{self.list_url}?author={self.author1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(book["author"] == self.author1.id for book in response.data))

    def test_search_books_by_title(self):
        """Ensure search by title works."""
        response = self.client.get(f"{self.list_url}?search=Book One")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Book One" in book["title"] for book in response.data))

    def test_order_books_by_publication_year(self):
        """Ensure ordering works."""
        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
