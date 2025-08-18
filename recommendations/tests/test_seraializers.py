from django.test import TestCase
from django.contrib.auth import get_user_model

from catalog.models import Book
from recommendations.models import Recommendation
from recommendations.api.serializers import RecommendationSerializer

User = get_user_model()


class RecommendationSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ser_user", password="pass")
        self.book = Book.objects.create(name="Ser Book", description="desc")
        self.rec = Recommendation.objects.create(user=self.user, book=self.book, score=77)

    def test_serialized_fields(self):
        serializer = RecommendationSerializer(self.rec)
        data = serializer.data
        self.assertIn('id', data)
        self.assertIn('user', data)
        self.assertIn('book_name', data)
        self.assertIn('book_image', data)
        self.assertIn('score', data)
        self.assertIn('created_at', data)

        self.assertEqual(data['user'], self.user.username)
        self.assertEqual(data['book_name'], self.book.name)
        self.assertEqual(data['score'], self.rec.score)

    def test_read_only_fields(self):
        meta = RecommendationSerializer.Meta
        self.assertEqual(tuple(meta.read_only_fields), tuple(meta.fields))
