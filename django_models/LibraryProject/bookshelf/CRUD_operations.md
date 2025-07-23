<<<<<<< HEAD:LibraryProject/bookshelf/CRUD_operations.md
## CREATE
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
# <Book: 1984 by George Orwell (1949)>

## RETRIEVE
retrieved_book = Book.objects.get(id=book.id)
retrieved_book.title, retrieved_book.author, retrieved_book.publication_year
# ('1984', 'George Orwell', 1949)

## UPDATE
book.title = "Nineteen Eighty-Four"
book.save()
book.title
# 'Nineteen Eighty-Four'

## DELETE
book.delete()
Book.objects.all()
# <QuerySet []>
=======
## CREATE
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
# <Book: 1984 by George Orwell (1949)>

## RETRIEVE
retrieved_book = Book.objects.get(id=book.id)
retrieved_book.title, retrieved_book.author, retrieved_book.publication_year
# ('1984', 'George Orwell', 1949)

## UPDATE
book.title = "Nineteen Eighty-Four"
book.save()
book.title
# 'Nineteen Eighty-Four'

## DELETE
book.delete()
Book.objects.all()
# <QuerySet []>
>>>>>>> 937340a0e06691c0104c1c6c6f649cad2fc5261b:Introduction_to_Django/LibraryProject/bookshelf/CRUD_operations.md
