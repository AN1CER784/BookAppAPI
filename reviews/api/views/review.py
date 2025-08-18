from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from common.mixins import AutoSchemaMixin
from reviews.api.serializers import BookReviewSerializer
from reviews.mixins import UserSerializerMixin
from reviews.models import BookReview


class ReviewViewSet(AutoSchemaMixin, UserSerializerMixin, viewsets.ModelViewSet):
    """
    ViewSet для работы с BookReview
    """
    model = BookReview
    queryset = BookReview.objects.with_votes().select_related('user', 'book')
    serializer_class = BookReviewSerializer
    permission_classes = (IsAuthenticated,)
    tags = ['reviews']
    params = {
        "book_pk": "ID book",
        "review_pk": "ID review",
    }