from django.test import TestCase

from catalog.models import Book, Author, Genre, BookLink


class BookModelTestCase(TestCase):
    def test_book_model(self):
        authors = [Author.objects.create(name=name) for name in ['Author1', 'Author2']]
        genres = [Genre.objects.create(name=name) for name in ['Genre1', 'Genre2']]

        book_links = [
            {'link': 'https://example.com/book1'},
            {'link': 'https://example.com/book2'}
        ]
        book = Book.objects.create(
            name='Test Book',
            description='Test Description',
        )
        book.authors.set(authors)
        book.genres.set(genres)
        for link in book_links:
            book.book_links.create(**link)
        self.assertEqual(book.name, 'Test Book')
        self.assertEqual(book.description, 'Test Description')
        self.assertEqual(list(book.authors.all()), authors)
        self.assertEqual(list(book.genres.all()), genres)
        self.assertEqual(list(BookLink.objects.values_list("link", flat=True)),
                         [link.get("link") for link in book_links])

    def test_author_model(self):
        author = Author.objects.create(name='Test Author', description="Test Description")
        self.assertEqual(author.name, 'Test Author')
        self.assertEqual(author.description, 'Test Description')

    def test_genre_model(self):
        genre = Genre.objects.create(name='Test Genre', description="Test Description")
        self.assertEqual(genre.name, 'Test Genre')
        self.assertEqual(genre.description, 'Test Description')
