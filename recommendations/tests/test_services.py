from django.test import TestCase
from django.contrib.auth import get_user_model
from catalog.models import Book, Author, Genre
from library.models import LibraryItem
from recommendations.models.recommendation import Recommendation
from recommendations.user_recommendation_service import RecommendationService

User = get_user_model()


class RecommendationServiceTestCase(TestCase):
    def setUp(self):
        # создаём пользователей
        self.user = User.objects.create_user(username="user1", password="pass")
        self.similar_user = User.objects.create_user(username="user2", password="pass")
        self.other_user = User.objects.create_user(username="user3", password="pass")

        # жанры и авторы
        self.genre_fantasy = Genre.objects.create(name="Fantasy")
        self.genre_detective = Genre.objects.create(name="Detective")

        self.author_tolstoy = Author.objects.create(name="Tolstoy")
        self.author_rowling = Author.objects.create(name="Rowling")
        self.author_doyle = Author.objects.create(name="Doyle")

        # книги пользователя
        self.book1 = Book.objects.create(name="War and Peace", description="Big book")
        self.book1.authors.add(self.author_tolstoy)
        self.book1.genres.add(self.genre_fantasy)
        LibraryItem.objects.create(book=self.book1, user=self.user)

        # книга похожего пользователя
        self.book2 = Book.objects.create(name="Harry Potter", description="Magic")
        self.book2.authors.add(self.author_rowling)
        self.book2.genres.add(self.genre_fantasy)
        LibraryItem.objects.create(book=self.book2, user=self.similar_user)

        # книга совсем другого пользователя
        self.book3 = Book.objects.create(name="Sherlock Holmes", description="Detective")
        self.book3.authors.add(self.author_doyle)
        self.book3.genres.add(self.genre_detective)
        LibraryItem.objects.create(book=self.book3, user=self.other_user)

        self.service = RecommendationService(self.user)

    def test_get_user_books(self):
        books = self.service._get_user_books()
        self.assertIn(self.book1, books)
        self.assertNotIn(self.book2, books)

    def test_get_user_preferences(self):
        prefs = self.service._get_user_preferences()
        self.assertIn(self.author_tolstoy, prefs['authors'])
        self.assertIn(self.genre_fantasy, prefs['genres'])

    def test_get_similar_users(self):
        prefs = self.service._get_user_preferences()
        users = self.service._get_similar_users(prefs)
        self.assertIn(self.similar_user, users)
        self.assertNotIn(self.other_user, users)

    def test_get_candidate_books(self):
        prefs = self.service._get_user_preferences()
        users = self.service._get_similar_users(prefs)
        candidates = self.service._get_candidate_books(users)
        self.assertIn(self.book2, candidates)
        self.assertNotIn(self.book1, candidates)  # исключается прочитанное

    def test_add_recommendations_creates_records(self):
        self.service.add_recommendations(limit=10)
        recs = Recommendation.objects.filter(user=self.user)
        self.assertTrue(recs.exists())
        self.assertIn(self.book2, [r.book for r in recs])
        self.assertNotIn(self.book1, [r.book for r in recs])
