from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from catalog.models import Book
from recommendations.models import Recommendation

User = get_user_model()


class RecommendationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u1", password="pass")
        self.other_user = User.objects.create_user(username="u2", password="pass")
        self.book = Book.objects.create(name="Test Book", description="desc")
        self.another_book = Book.objects.create(name="Another Book", description="desc2")

    def test_create_recommendation(self):
        rec = Recommendation.objects.create(user=self.user, book=self.book, score=50)
        self.assertIsNotNone(rec.pk)
        self.assertEqual(rec.user, self.user)
        self.assertEqual(rec.book, self.book)
        self.assertEqual(rec.score, 50)

    def test_book_one_to_one_enforced(self):
        Recommendation.objects.create(user=self.user, book=self.book, score=10)
        # попытка создать вторую рекомендацию для той же книги должна падать (OneToOne)
        with self.assertRaises(IntegrityError):
            Recommendation.objects.create(user=self.other_user, book=self.book, score=20)
