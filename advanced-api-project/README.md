### API Endpoints
- GET /api/books/ → List all books.
- GET /api/books/<id>/ → Retrieve a single book.
- POST /api/books/create/ → Add a new book (auth required).
- PATCH/PUT /api/books/<id>/update/ → Update a book (auth required).
- DELETE /api/books/<id>/delete/ → Delete a book (auth required).

Permissions:
- Unauthenticated users → Read only.
- Authenticated users → Create, update, delete.

### Filtering
GET /api/books/?title=BookTitle
GET /api/books/?author=1
GET /api/books/?publication_year=2023

### Searching
GET /api/books/?search=keyword

### Ordering
GET /api/books/?ordering=title
GET /api/books/?ordering=-publication_year

### Running Tests
To run the API unit tests:
    python manage.py test api

Tests cover:
- CRUD operations for Book model
- Filtering, searching, and ordering
- Permissions: authenticated vs unauthenticated access
- Data validation and correct status codes
