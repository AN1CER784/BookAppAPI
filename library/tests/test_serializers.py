from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from library.models import LibraryItem, Progress
from catalog.models import Book
from library.api.serializers import ProgressSerializer, LibraryItemSerializer

User = get_user_model()


class ProgressSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="1234")
        self.book = Book.objects.create(name="Book 1")
        self.item = LibraryItem.objects.create(user=self.user, book=self.book)

    def test_serialize_progress(self):
        progress = Progress.objects.create(library_item=self.item, complete_percentage=40)
        serializer = ProgressSerializer(progress)
        self.assertEqual(serializer.data, {"complete_percentage": 40})

    def test_validate_invalid_progress(self):
        serializer = ProgressSerializer(data={"complete_percentage": 150})
        self.assertFalse(serializer.is_valid())
        self.assertIn("complete_percentage", serializer.errors)


class LibraryItemSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="1234")
        image = SimpleUploadedFile("cover.jpg", b"filecontent", content_type="image/jpeg")
        self.book = Book.objects.create(name="Book Name", image=image)

    def test_create_library_item(self):
        data = {"book_id": self.book.id}
        serializer = LibraryItemSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        item = serializer.save(user=self.user)
        self.assertEqual(item.book, self.book)
        self.assertEqual(item.user, self.user)

    def test_serialize_library_item_with_nested_fields(self):
        item = LibraryItem.objects.create(user=self.user, book=self.book)
        Progress.objects.create(library_item=item, complete_percentage=75)

        serializer = LibraryItemSerializer(item)
        data = serializer.data

        self.assertEqual(data["id"], item.id)
        self.assertEqual(data["book"]["name"], self.book.name)
        self.assertIn("image", data["book"])

        self.assertEqual(data["progress"]["complete_percentage"], 75)

    def test_user_is_readonly(self):
        data = {"book_id": self.book.id, "user": 999}
        serializer = LibraryItemSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        item = serializer.save(user=self.user)
        self.assertEqual(item.user, self.user)
