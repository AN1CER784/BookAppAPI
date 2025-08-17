from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import ValidationError as DRFValidationError

from reviews.api.serializers.vote import VoteValueField
from reviews.models import Vote, Reply, BookReview
from reviews.api.serializers import VoteSerializer, ReplySerializer, BookReviewSerializer
from catalog.models import Book

User = get_user_model()


class VoteValueFieldTests(TestCase):
    def setUp(self):
        self.field = VoteValueField()

    def test_to_representation(self):
        self.assertEqual(self.field.to_representation(1), "LIKE")
        self.assertEqual(self.field.to_representation(-1), "DISLIKE")

    def test_to_internal_value_accepts_labels(self):
        self.assertEqual(self.field.to_internal_value("LIKE"), 1)
        self.assertEqual(self.field.to_internal_value("like"), 1)
        self.assertEqual(self.field.to_internal_value(" DISLIKE "), -1)
        self.assertEqual(self.field.to_internal_value("disLike"), -1)

    def test_to_internal_value_accepts_numbers(self):
        self.assertEqual(self.field.to_internal_value(1), 1)
        self.assertEqual(self.field.to_internal_value(-1), -1)
        self.assertEqual(self.field.to_internal_value("1"), 1)
        self.assertEqual(self.field.to_internal_value("-1"), -1)

    def test_to_internal_value_invalid(self):
        with self.assertRaises(Exception):
            # будет вызывать ValidationError через fail(...)
            self.field.to_internal_value("unknown")

        with self.assertRaises(Exception):
            self.field.to_internal_value(999)


class VoteSerializerTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username="u1", password="p")
        self.book = Book.objects.create(name="B1")
        self.review = BookReview.objects.create(user=self.user, book=self.book, rating=5, text="r")

    def test_create_vote_success(self):
        request = self.factory.post("/")
        request.user = self.user

        serializer = VoteSerializer(data={'value': 'LIKE'}, context={'request': request})
        self.assertTrue(serializer.is_valid(), serializer.errors)

        ct = ContentType.objects.get_for_model(BookReview)
        vote = serializer.save(content_type=ct, object_id=self.review.id)

        self.assertIsInstance(vote, Vote)
        self.assertEqual(vote.user, self.user)
        self.assertEqual(vote.value, 1)
        self.assertEqual(vote.content_type, ct)
        self.assertEqual(vote.object_id, self.review.id)

    def test_create_vote_duplicate_raises(self):
        Vote.objects.create(user=self.user, value=1,
                            content_type=ContentType.objects.get_for_model(BookReview),
                            object_id=self.review.id)

        request = self.factory.post("/")
        request.user = self.user

        serializer = VoteSerializer(data={'value': 'LIKE'}, context={'request': request})
        self.assertTrue(serializer.is_valid(), serializer.errors)

        ct = ContentType.objects.get_for_model(BookReview)
        with self.assertRaises(DRFValidationError):
            serializer.save(content_type=ct, object_id=self.review.id)


class ReplyAndBookReviewSerializerTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user1 = User.objects.create_user(username="u1", password="p")
        self.user2 = User.objects.create_user(username="u2", password="p")
        self.book = Book.objects.create(name="Book name 1")
        self.review = BookReview.objects.create(user=self.user1, book=self.book, rating=7, text="good")

    def test_reply_create_and_serialization_with_votes(self):
        request = self.factory.post("/")
        request.user = self.user2

        serializer = ReplySerializer(data={'text': 'my reply', 'review_id': self.review.id},
                                     context={'request': request})
        self.assertTrue(serializer.is_valid(), serializer.errors)

        ct = ContentType.objects.get_for_model(BookReview)
        reply = serializer.save(user=self.user2, content_type=ct, object_id=self.review.id)

        self.assertEqual(reply.user, self.user2)
        self.assertEqual(reply.review, self.review)
        self.assertEqual(reply.object_id, self.review.id)
        self.assertEqual(reply.content_type, ct)
        reply.votes.create(user=self.user1, value=1)
        reply.votes.create(user=self.user2, value=-1)
        annotated = Reply.objects.with_votes().get(pk=reply.pk)
        ser = ReplySerializer(annotated)
        data = ser.data

        self.assertEqual(data['id'], reply.id)
        self.assertEqual(data['user'], self.user2.username)
        self.assertEqual(data['likes_count'], 1)
        self.assertEqual(data['dislikes_count'], 1)
        self.assertIn('content_type', data)
        self.assertIn('object_id', data)

    def test_bookreview_create_and_annotated_counts(self):
        request = self.factory.post("/")
        request.user = self.user2

        new_book = Book.objects.create(name="Book Two")
        data = {'book_id': new_book.id, 'rating': 8, 'text': 'nice'}
        ser = BookReviewSerializer(data=data, context={'request': request})
        self.assertTrue(ser.is_valid(), ser.errors)

        review_obj = ser.save(user=self.user2)

        self.assertEqual(review_obj.book, new_book)
        self.assertEqual(review_obj.user, self.user2)
        self.assertEqual(review_obj.rating, 8)
        self.assertEqual(review_obj.text, 'nice')

        review_obj.votes.create(user=self.user1, value=1)
        review_obj.votes.create(user=self.user2, value=1)

        annotated = BookReview.objects.with_votes().get(pk=review_obj.pk)
        ser2 = BookReviewSerializer(annotated)
        data2 = ser2.data

        self.assertEqual(data2['likes_count'], 2)
        self.assertEqual(data2['dislikes_count'], 0)
        self.assertEqual(data2['book'], new_book.name)
        self.assertEqual(data2['user'], self.user2.username)
