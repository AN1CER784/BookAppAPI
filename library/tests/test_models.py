from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from library.models import LibraryItem, Progress
from catalog.models import Book

User = get_user_model()


class LibraryItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="1234")
        self.book = Book.objects.create(name="Test Book")

    def test_create_library_item(self):
        item = LibraryItem.objects.create(user=self.user, book=self.book)
        self.assertEqual(item.user, self.user)
        self.assertEqual(item.book, self.book)

    def test_unique_book_constraint(self):
        LibraryItem.objects.create(user=self.user, book=self.book)
        with self.assertRaises(Exception):
            LibraryItem.objects.create(user=self.user, book=self.book)


class ProgressModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="1234")
        self.book = Book.objects.create(name="Test Book")
        self.item = LibraryItem.objects.create(user=self.user, book=self.book)

    def test_progress_default_value(self):
        progress = Progress.objects.create(library_item=self.item)
        self.assertEqual(progress.complete_percentage, 0)

    def test_progress_validators(self):
        progress = Progress(library_item=self.item, complete_percentage=-1)
        with self.assertRaises(ValidationError):
            progress.full_clean()

        progress = Progress(library_item=self.item, complete_percentage=101)
        with self.assertRaises(ValidationError):
            progress.full_clean()

    def test_one_to_one_relation(self):
        Progress.objects.create(library_item=self.item, complete_percentage=10)
        with self.assertRaises(Exception):
            Progress.objects.create(library_item=self.item, complete_percentage=20)

