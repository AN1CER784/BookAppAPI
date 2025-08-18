from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from catalog.models import Genre
from catalog.permissions import IsAdminOrAuthenticatedReadOnly
from catalog.api.serializers import GenreSerializer
from common.mixins import AutoSchemaMixin


class GenreAPIViewSet(AutoSchemaMixin, viewsets.ModelViewSet):
    """
    ViewSet для работы с жанрами
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    tags = ['catalog/authors']