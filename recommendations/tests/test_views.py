from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Book
from recommendations.models import Recommendation

User = get_user_model()


class RecommendationViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="auser", password="pw")
        self.other = User.objects.create_user(username="other", password="pw")

        self.book1 = Book.objects.create(name="Book 1", description="d1")
        self.book2 = Book.objects.create(name="Book 2", description="d2")
        self.book3 = Book.objects.create(name="Book 3", description="d3")

        Recommendation.objects.create(user=self.user, book=self.book1, score=10)
        Recommendation.objects.create(user=self.user, book=self.book2, score=5)
        Recommendation.objects.create(user=self.other, book=self.book3, score=99)

        self.client.force_authenticate(user=None)

    def test_unauthenticated_cannot_access(self):
        url = reverse('recommendations:user-recommendations-list')
        resp = self.client.get(url)
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_authenticated_sees_only_own_recommendations_and_ordered(self):
        url = reverse('recommendations:user-recommendations-list')
        self.client.force_authenticate(user=self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()["results"]
        self.assertEqual(len(data), 2)
        scores = [item['score'] for item in data]
        self.assertTrue(all(scores[i] >= scores[i + 1] for i in range(len(scores) - 1)))
        returned_books = {item['book_name'] for item in data}
        self.assertNotIn(self.book3.name, returned_books)
        self.assertIn(self.book1.name, returned_books)
        self.assertIn(self.book2.name, returned_books)
