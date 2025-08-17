from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from catalog.api.serializers import BookCreateSerializer, BookSerializer
from catalog.api.views import BookAPIViewSet
from catalog.models import Author, Genre, Book, BookLink

User = get_user_model()


class TestPermissionsOnViewSet(APITestCase):
    url = None
    create_data = None

    # Ожидаемые коды — можно переопределять в подклассах
    anonymous_status = status.HTTP_401_UNAUTHORIZED
    authenticated_create_status = status.HTTP_403_FORBIDDEN
    admin_create_status = status.HTTP_201_CREATED

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="user", email="u@test", password="1234")
        cls.admin = User.objects.create_superuser(username="admin", email="a@test", password="1234")

    def get_client(self):
        return APIClient()

    def test_anonymous(self):
        client = self.get_client()
        resp = client.get(self.url)
        self.assertEqual(resp.status_code, self.anonymous_status)

    def test_authenticated_user_can_list_but_cannot_create(self):
        client = self.get_client()
        client.force_authenticate(user=self.user)

        resp = client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = client.post(self.url, self.create_data or {}, format='json')
        self.assertEqual(resp.status_code, self.authenticated_create_status)

    def test_admin_can_create(self):
        client = self.get_client()
        client.force_authenticate(user=self.admin)
        resp = client.post(self.url, self.create_data or {}, format='json')
        self.assertEqual(resp.status_code, self.admin_create_status)

        if resp.status_code == status.HTTP_201_CREATED:
            created_name = resp.data.get('name')
            self.assertIsNotNone(created_name)


class AuthorAPIViewSetTestCase(TestPermissionsOnViewSet):
    def setUp(self):
        self.url = reverse('catalog:authors-list')
        self.create_data = {"name": "New Author"}


class GenreAPIViewSetTestCase(TestPermissionsOnViewSet):
    def setUp(self):
        self.url = reverse('catalog:genres-list')
        self.create_data = {"name": "New Genre"}


class BookAPIViewSetTestCase(TestPermissionsOnViewSet):
    def setUp(self):
        self.author = Author.objects.create(name="Author X")
        self.genre = Genre.objects.create(name="Genre Y")
        self.book = Book.objects.create(name="Book 1", description="Desc")
        self.book.authors.add(self.author)
        self.book.genres.add(self.genre)
        self.book_link = BookLink.objects.create(book=self.book, link="http://x.com")
        self.url = reverse('catalog:books-list')
        self.create_data = {"name": "Book 1", "authors": [{'name': 'Test Author'}], "genres": [{'name': 'Test Genre'}],
                            "book_links": [{'link': "http://x.com"}]}

    def test_download_action_returns_links(self):
        self.client.login(username="user", password="1234")
        url = reverse("catalog:books-download", args=[self.book.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("book_links", resp.data)
        self.assertEqual(resp.data["book_links"][0]["link"], "http://x.com")

    def test_get_serializer_class_for_create(self):
        view = BookAPIViewSet()
        view.action = "create"
        self.assertIs(view.get_serializer_class(), BookCreateSerializer)

    def test_get_serializer_class_for_list(self):
        view = BookAPIViewSet()
        view.action = "list"
        self.assertIs(view.get_serializer_class(), BookSerializer)
