from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, permissions

from common.mixins import AutoSchemaMixin
from reviews.api.serializers import VoteSerializer
from reviews.models import BookReview, Reply, Vote


class ReviewVoteViewSet(AutoSchemaMixin, viewsets.ModelViewSet):
    """
    ViewSet для работы с голосами по отзывам
    """
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    tags = ['reviews/votes']
    params = {
        "book_pk": "ID book",
        "review_pk": "ID review",
    }

    def get_queryset(self):
        return Vote.objects.filter(content_type=ContentType.objects.get_for_model(BookReview),
                                   object_id=self.kwargs['review_pk']).select_related('content_type', 'user')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, content_type=ContentType.objects.get_for_model(BookReview),
                        object_id=self.kwargs['review_pk'])


class ReplyVoteViewSet(AutoSchemaMixin, viewsets.ModelViewSet):
    """
    ViewSet для работы с голосами по ответам
    """
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    tags = ['replies/votes']
    params = {
        "book_pk": "ID book",
        "review_pk": "ID review",
        "reply_pk": "ID reply",
        "parent_reply_pk": "ID parent pk",
        "child_reply_pk": "ID child pk",
    }

    def get_queryset(self):
        object_id = self.kwargs.get("parent_reply_pk") or self.kwargs.get("child_reply_pk")
        return Vote.objects.filter(content_type=ContentType.objects.get_for_model(Reply),
                                   object_id=object_id).select_related('content_type', 'user')

    def perform_create(self, serializer):
        object_id = self.kwargs.get("parent_reply_pk") or self.kwargs.get("child_reply_pk")
        serializer.save(user=self.request.user, content_type=ContentType.objects.get_for_model(Reply),
                        object_id=object_id)
