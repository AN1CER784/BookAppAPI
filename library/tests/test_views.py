from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from catalog.models import Book
from library.models import LibraryItem, Progress

User = get_user_model()


class LibraryItemViewSetTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('library:books-list')

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="user", email="u@test", password="1234")
        cls.book = Book.objects.create(name="Test Book")

    def get_client(self, auth=False):
        client = APIClient()
        if auth:
            client.force_authenticate(user=self.user)
        return client

    def test_anonymous(self):
        client = self.get_client()
        resp = client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_library_item(self):
        client = self.get_client(auth=True)
        data = {"book_id": self.book.id}
        resp = client.post(self.url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_list_library_items(self):
        item = LibraryItem.objects.create(user=self.user, book=self.book)
        Progress.objects.create(library_item=item)
        client = self.get_client(auth=True)
        resp = client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


    def test_progress_get_and_patch(self):
        item = LibraryItem.objects.create(user=self.user, book=self.book)
        progress = Progress.objects.create(library_item=item, complete_percentage=10)
        client = self.get_client(auth=True)

        url = reverse('library:books-progress', args=[item.id])
        resp = client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['complete_percentage'], 10)

        resp = client.patch(url, {"complete_percentage": 50}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        progress.refresh_from_db()
        self.assertEqual(progress.complete_percentage, 50)

    def test_active_items(self):
        item = LibraryItem.objects.create(user=self.user, book=self.book)
        Progress.objects.create(library_item=item, complete_percentage=50)

        client = self.get_client(auth=True)
        url = reverse('library:books-active-items')
        resp = client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(resp.json()[0]['id'], item.id)

    def test_done_items(self):
        item = LibraryItem.objects.create(user=self.user, book=self.book)
        Progress.objects.create(library_item=item, complete_percentage=100)

        client = self.get_client(auth=True)
        url = reverse('library:books-done-items')
        resp = client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(resp.json()[0]['id'], item.id)
