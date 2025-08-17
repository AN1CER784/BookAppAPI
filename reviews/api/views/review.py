from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from reviews.api.serializers import BookReviewSerializer
from reviews.mixins import UserSerializerMixin
from reviews.models import BookReview


class ReviewViewSet(UserSerializerMixin, viewsets.ModelViewSet):
    """
    ViewSet для работы с BookReview
    """
    model = BookReview
    queryset = BookReview.objects.with_votes().select_related('user', 'book')
    serializer_class = BookReviewSerializer
    permission_classes = (IsAuthenticated,)
