from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from catalog.models import Book
from reviews.models import BookReview, Reply, Vote
from reviews.api.views import ReviewViewSet, ReplyViewSet, ReviewVoteViewSet, ReplyVoteViewSet

User = get_user_model()


class ReviewViewSetTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username="u1", password="p")
        self.other = User.objects.create_user(username="u2", password="p")
        self.book = Book.objects.create(name="B1")

    def test_list_requires_auth(self):
        view = ReviewViewSet.as_view({'get': 'list'})
        request = self.factory.get('/')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_returns_reviews_with_votes(self):
        r1 = BookReview.objects.create(user=self.user, book=self.book, rating=5, text="r1")
        r2 = BookReview.objects.create(user=self.other, book=self.book, rating=6, text="r2")
        r1.votes.create(user=self.user, value=1)
        r1.votes.create(user=self.other, value=-1)
        view = ReviewViewSet.as_view({'get': 'list'})
        request = self.factory.get('/')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data["results"]
        ids = {item['id'] for item in data}
        self.assertIn(r1.id, ids)
        r1_data = next(item for item in data if item['id'] == r1.id)
        self.assertEqual(r1_data['likes_count'], 1)
        self.assertEqual(r1_data['dislikes_count'], 1)
        self.assertEqual(r1_data['user'], self.user.username)
        self.assertEqual(r1_data['book'], self.book.name)

    def test_create_review(self):
        view = ReviewViewSet.as_view({'post': 'create'})
        payload = {'book_id': self.book.id, 'rating': 8, 'text': 'nice'}
        request = self.factory.post('/', payload, format='json')
        force_authenticate(request, user=self.other)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        obj = BookReview.objects.get(pk=response.data['id'])
        self.assertEqual(obj.user, self.other)
        self.assertEqual(obj.book, self.book)
        self.assertEqual(obj.rating, 8)


class ReplyViewSetTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username="u1", password="p")
        self.user2 = User.objects.create_user(username="u2", password="p")
        self.book = Book.objects.create(name="B1")
        self.review = BookReview.objects.create(user=self.user, book=self.book, rating=7, text="rev")

    def test_list_replies_for_review(self):
        r1 = Reply.objects.create(user=self.user2, review=self.review, text="r1",
                                  content_type=ContentType.objects.get_for_model(BookReview),
                                  object_id=self.review.id)
        r2 = Reply.objects.create(user=self.user2, review=self.review, text="r2",
                                  content_type=ContentType.objects.get_for_model(BookReview),
                                  object_id=self.review.id)
        view = ReplyViewSet.as_view({'get': 'list'})
        request = self.factory.get('/')
        force_authenticate(request, user=self.user)
        response = view(request, review_pk=self.review.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        ids = {item['id'] for item in response.data["results"]}
        self.assertIn(r1.id, ids)
        self.assertIn(r2.id, ids)

    def test_create_reply_for_review(self):
        view = ReplyViewSet.as_view({'post': 'create'})
        payload = {'text': 'my reply', 'review_id': self.review.id}
        request = self.factory.post('/', payload, format='json')
        force_authenticate(request, user=self.user2)
        response = view(request, review_pk=self.review.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reply = Reply.objects.get(pk=response.data['id'])
        self.assertEqual(reply.user, self.user2)
        self.assertEqual(reply.review, self.review)
        self.assertEqual(reply.object_id, self.review.id)
        self.assertEqual(reply.content_type, ContentType.objects.get_for_model(BookReview))

    def test_create_reply_to_reply(self):
        parent = Reply.objects.create(user=self.user2, review=self.review, text="parent",
                                      content_type=ContentType.objects.get_for_model(BookReview),
                                      object_id=self.review.id)
        view = ReplyViewSet.as_view({'post': 'create'})
        payload = {'text': 'child reply', 'review_id': parent.review.id}
        request = self.factory.post('/', payload, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, reply_pk=parent.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        child = Reply.objects.get(pk=response.data['id'])
        self.assertEqual(child.content_type, ContentType.objects.get_for_model(Reply))
        self.assertEqual(child.object_id, parent.id)
        self.assertEqual(child.user, self.user)


class VoteViewSetTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username="u1", password="p")
        self.user2 = User.objects.create_user(username="u2", password="p")
        self.book = Book.objects.create(name="B1")
        self.review = BookReview.objects.create(user=self.user2, book=self.book, rating=6, text="rev2")
        self.reply = Reply.objects.create(user=self.user, review=self.review, text="r",
                                          content_type=ContentType.objects.get_for_model(BookReview),
                                          object_id=self.review.id)

    def test_create_vote_for_review(self):
        view = ReviewVoteViewSet.as_view({'post': 'create', 'get': 'list'})
        payload = {'value': 'LIKE'}
        request = self.factory.post('/', payload, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, review_pk=self.review.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        v = Vote.objects.get(pk=response.data['id'])
        self.assertEqual(v.user, self.user)
        self.assertEqual(v.value, 1)
        self.assertEqual(v.content_type, ContentType.objects.get_for_model(BookReview))
        self.assertEqual(v.object_id, self.review.id)

    def test_duplicate_vote_for_review_returns_400(self):
        Vote.objects.create(user=self.user, value=1,
                            content_type=ContentType.objects.get_for_model(BookReview),
                            object_id=self.review.id)
        view = ReviewVoteViewSet.as_view({'post': 'create'})
        payload = {'value': 'LIKE'}
        request = self.factory.post('/', payload, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, review_pk=self.review.id)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_vote_for_reply(self):
        view = ReplyVoteViewSet.as_view({'post': 'create', 'get': 'list'})
        payload = {'value': -1}
        request = self.factory.post('/', payload, format='json')
        force_authenticate(request, user=self.user2)
        response = view(request, parent_reply_pk=self.reply.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        v = Vote.objects.get(pk=response.data['id'])
        self.assertEqual(v.user, self.user2)
        self.assertEqual(v.value, -1)
        self.assertEqual(v.content_type, ContentType.objects.get_for_model(Reply))
        self.assertEqual(v.object_id, self.reply.id)

    def test_list_votes_for_review(self):
        Vote.objects.create(user=self.user, value=1,
                            content_type=ContentType.objects.get_for_model(BookReview),
                            object_id=self.review.id)
        Vote.objects.create(user=self.user2, value=-1,
                            content_type=ContentType.objects.get_for_model(BookReview),
                            object_id=self.review.id)
        view = ReviewVoteViewSet.as_view({'get': 'list'})
        request = self.factory.get('/')
        force_authenticate(request, user=self.user)
        response = view(request, review_pk=self.review.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data["results"]

        self.assertEqual(len(data), 2)
        values = {item['value'] for item in data}
        self.assertTrue('LIKE' in values or 1 in values)
