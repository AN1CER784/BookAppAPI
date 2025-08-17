from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.test import TestCase

from catalog.models import Book  # путь к модели Book в проекте
from reviews.models import Vote, BookReview, Reply  # подстрой путь, если нужно

User = get_user_model()


class BaseMessageQuerySetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username="u1", password="pass")
        cls.user2 = User.objects.create_user(username="u2", password="pass")
        cls.user3 = User.objects.create_user(username="u3", password="pass")

        cls.book = Book.objects.create(name="Test Book")

        cls.review1 = BookReview.objects.create(user=cls.user1, book=cls.book, rating=5, text="R1")
        cls.review2 = BookReview.objects.create(user=cls.user2, book=cls.book, rating=6, text="R2")
        cls.review3 = BookReview.objects.create(user=cls.user3, book=cls.book, rating=7, text="R3")
        cls.review4 = BookReview.objects.create(user=cls.user1, book=Book.objects.create(name="Other Book"), rating=8,
                                                text="R4")

        cls.review1.votes.create(user=cls.user1, value=1)
        cls.review1.votes.create(user=cls.user2, value=1)
        cls.review1.votes.create(user=cls.user3, value=-1)

        cls.review2.votes.create(user=cls.user1, value=1)

        cls.review4.votes.create(user=cls.user2, value=1)
        cls.review4.votes.create(user=cls.user3, value=1)

        extra1 = User.objects.create_user(username="extra1", password="p")
        extra2 = User.objects.create_user(username="extra2", password="p")
        cls.review4.votes.create(user=extra1, value=-1)
        cls.review4.votes.create(user=extra2, value=-1)

    def test_with_votes_annotation_and_counts(self):
        qs = BookReview.objects.with_votes()
        items = list(qs)

        ids = [i.id for i in items]
        self.assertIn(self.review1.id, ids)
        self.assertIn(self.review2.id, ids)
        self.assertIn(self.review3.id, ids)
        self.assertIn(self.review4.id, ids)

        by_id = {obj.id: obj for obj in items}

        self.assertEqual(getattr(by_id[self.review1.id], 'likes_count'), 2)
        self.assertEqual(getattr(by_id[self.review1.id], 'dislikes_count'), 1)

        self.assertEqual(getattr(by_id[self.review2.id], 'likes_count'), 1)
        self.assertEqual(getattr(by_id[self.review2.id], 'dislikes_count'), 0)

        self.assertEqual(getattr(by_id[self.review3.id], 'likes_count'), 0)
        self.assertEqual(getattr(by_id[self.review3.id], 'dislikes_count'), 0)

        self.assertEqual(getattr(by_id[self.review4.id], 'likes_count'), 2)
        self.assertEqual(getattr(by_id[self.review4.id], 'dislikes_count'), 2)

    def test_with_votes_ordering(self):
        qs = BookReview.objects.with_votes()
        ordered = list(qs)

        pos4 = ordered.index(self.review4)
        pos1 = ordered.index(self.review1)
        pos2 = ordered.index(self.review2)
        pos3 = ordered.index(self.review3)

        self.assertLess(pos4, pos1)  # review4 выше review1 из-за большего dislikes_count
        self.assertLess(pos1, pos2)  # review1 (2 likes) выше review2 (1 like)
        self.assertLess(pos2, pos3)  # review2 (1 like) выше review3 (0 like)

    def test_vote_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            Vote.objects.create(user=self.user1, value=1,
                                content_type=ContentType.objects.get_for_model(BookReview),
                                object_id=self.review1.id)

    def test_votes_on_reply_counted_separately(self):
        reply = Reply.objects.create(user=self.user2, review=self.review1, text="reply text",
                                     content_type=ContentType.objects.get_for_model(BookReview),
                                     object_id=self.review1.id)

        reply.votes.create(user=self.user1, value=1)
        reply.votes.create(user=self.user3, value=-1)

        reply_qs = Reply.objects.with_votes()
        reply_list = list(reply_qs)
        self.assertIn(reply.id, [r.id for r in reply_list])

        by_id = {obj.id: obj for obj in reply_list}
        self.assertEqual(getattr(by_id[reply.id], 'likes_count'), 1)
        self.assertEqual(getattr(by_id[reply.id], 'dislikes_count'), 1)
