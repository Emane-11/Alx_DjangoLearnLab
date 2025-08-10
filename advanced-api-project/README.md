### API Endpoints
- GET /api/books/ → List all books.
- GET /api/books/<id>/ → Retrieve a single book.
- POST /api/books/create/ → Add a new book (auth required).
- PATCH/PUT /api/books/<id>/update/ → Update a book (auth required).
- DELETE /api/books/<id>/delete/ → Delete a book (auth required).

Permissions:
- Unauthenticated users → Read only.
- Authenticated users → Create, update, delete.
