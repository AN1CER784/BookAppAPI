from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from reviews.api.serializers import ReplySerializer
from reviews.mixins import UserSerializerMixin
from reviews.models import BookReview, Reply


class ReplyViewSet(UserSerializerMixin, viewsets.ModelViewSet):
    """
    ViewSet для работы с ответами
    """
    model = Reply
    queryset = Reply.objects.with_votes()
    serializer_class = ReplySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        review_pk = self.kwargs.get("review_pk")
        reply_pk = self.kwargs.get("reply_pk")
        if reply_pk:
            queryset = Reply.objects.filter(content_type=ContentType.objects.get_for_model(Reply), object_id=reply_pk)
        elif review_pk:
            queryset = Reply.objects.filter(content_type=ContentType.objects.get_for_model(BookReview), object_id=review_pk)
        else:
            return None
        return queryset.select_related('user', 'content_type')

    def perform_create(self, serializer):
        review_pk = self.kwargs.get("review_pk")
        reply_pk = self.kwargs.get("reply_pk")
        if reply_pk:
            serializer.save(content_type=ContentType.objects.get_for_model(Reply), object_id=reply_pk,
                            user=self.request.user)
        elif review_pk:
            serializer.save(content_type=ContentType.objects.get_for_model(BookReview), object_id=review_pk,
                            user=self.request.user)
