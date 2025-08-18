from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from catalog.models import Author
from catalog.permissions import IsAdminOrAuthenticatedReadOnly
from catalog.api.serializers import AuthorSerializer
from common.mixins import AutoSchemaMixin


class AuthorAPIViewSet(AutoSchemaMixin, viewsets.ModelViewSet):
    """
    ViewSet для работы с авторами
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    tags = ['catalog/authors']