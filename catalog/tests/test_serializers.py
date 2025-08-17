from django.test import TestCase

from catalog.api.serializers import BookCreateSerializer, BookSerializer, AuthorSerializer, GenreSerializer
from catalog.models import Book, Author, Genre, BookLink


class BookCreateSerializerTestCase(TestCase):
    def test_create(self):
        data = {
            'name': 'Test Book',
            'description': 'Test Description',
            'authors': [{'name': 'Test Author'}],
            'genres': [{'name': 'Test Genre'}],
            'book_links': [{'link': 'https://example.com/test'}],
        }
        serializer = BookCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        book = serializer.save()
        self.assertEqual(book.name, 'Test Book')
        self.assertEqual(book.description, 'Test Description')
        self.assertEqual(book.authors.count(), 1)
        self.assertEqual(book.authors.first().name, 'Test Author')
        self.assertEqual(book.genres.count(), 1)
        self.assertEqual(book.genres.first().name, 'Test Genre')
        self.assertEqual(book.book_links.count(), 1)
        self.assertEqual(book.book_links.first().link, 'https://example.com/test')

    def test_update(self):
        book = Book.objects.create(name='Test Book', description='Test Description')
        data = {
            'name': 'Updated Book',
            'description': 'Updated Description',
            'authors': [{'name': 'Updated Author'}],
            'genres': [{'name': 'Updated Genre'}],
            'book_links': [{'link': 'https://example.com/test'}],
        }
        serializer = BookCreateSerializer(instance=book, data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        book = serializer.save()
        self.assertEqual(book.name, 'Updated Book')
        self.assertEqual(book.description, 'Updated Description')
        self.assertEqual(book.authors.count(), 1)
        self.assertEqual(book.authors.first().name, 'Updated Author')
        self.assertEqual(book.genres.count(), 1)
        self.assertEqual(book.genres.first().name, 'Updated Genre')
        self.assertEqual(book.book_links.count(), 1)
        self.assertEqual(book.book_links.first().link, 'https://example.com/test')

    def test_invalid_create(self):
        data = {
            'name': 'Test Book',
            'description': 'Test Description',
        }
        serializer = BookCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('authors', serializer.errors)
        self.assertIn('genres', serializer.errors)
        self.assertIn('book_links', serializer.errors)

    def test_invalid_update(self):
        book = Book.objects.create(name='Test Book', description='Test Description')
        data = {
            'name': 'Updated Book',
            'description': 'Updated Description',
        }
        serializer = BookCreateSerializer(instance=book, data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('authors', serializer.errors)
        self.assertIn('genres', serializer.errors)
        self.assertIn('book_links', serializer.errors)


class BookSerializerTestCase(TestCase):
    def test_get_serializer(self):
        author1 = Author.objects.create(name="Author One")
        author2 = Author.objects.create(name="Author Two")
        genre1 = Genre.objects.create(name="Fantasy")
        genre2 = Genre.objects.create(name="Sci-Fi")
        book = Book.objects.create(name="Test Book", description="Some description")
        link = BookLink.objects.create(link='https://example.com/test', book=book)
        book.authors.add(author1, author2)
        book.genres.add(genre1, genre2)
        book.book_links.add(link)
        serializer = BookSerializer(book)

        data = serializer.data
        self.assertEqual(data['name'], 'Test Book')
        self.assertEqual(data['description'], 'Some description')
        self.assertEqual(len(data['authors']), 2)
        self.assertIn('Author One', data['authors'])
        self.assertIn('Author Two', data['authors'])
        self.assertEqual(len(data['genres']), 2)
        self.assertIn('Fantasy', data['genres'])
        self.assertIn('Sci-Fi', data['genres'])
        self.assertIn(data['book_links'], '/api/v1/catalog/books/1/download/')


class AuthorSerializerTestCase(TestCase):
    def test_create_serializer(self):
        data = {
            'name': 'Test Author',
            'description': 'Test description',
        }
        serializer = AuthorSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        author = serializer.save()
        self.assertEqual(author.name, 'Test Author')
        self.assertEqual(author.description, 'Test description')

    def test_update_serializer(self):
        author = Author.objects.create(name='Test Author', description='Test description')
        data = {
            'name': 'Updated Author',
            'description': 'Updated description',
        }
        serializer = AuthorSerializer(instance=author, data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        author = serializer.save()
        self.assertEqual(author.name, 'Updated Author')
        self.assertEqual(author.description, 'Updated description')

    def test_get_serializer(self):
        author = Author.objects.create(name='Test Author', description='Test description')
        serializer = AuthorSerializer(author)
        data = serializer.data
        self.assertEqual(data['name'], 'Test Author')
        self.assertEqual(data['description'], 'Test description')


class GenreSerializerTestCase(TestCase):
    def test_create_serializer(self):
        data = {
            'name': 'Test Genre',
            'description': 'Test description',
        }
        serializer = GenreSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        genre = serializer.save()
        self.assertEqual(genre.name, 'Test Genre')
        self.assertEqual(genre.description, 'Test description')

    def test_update_serializer(self):
        genre = Genre.objects.create(name='Test Genre', description='Test description')
        data = {
            'name': 'Updated Genre',
            'description': 'Updated description',
        }
        serializer = GenreSerializer(instance=genre, data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        genre = serializer.save()
        self.assertEqual(genre.name, 'Updated Genre')
        self.assertEqual(genre.description, 'Updated description')

    def test_get_serializer(self):
        genre = Genre.objects.create(name='Test Genre', description='Test description')
        serializer = GenreSerializer(genre)
        genre = serializer.data
        self.assertEqual(genre['name'], 'Test Genre')
        self.assertEqual(genre['description'], 'Test description')
