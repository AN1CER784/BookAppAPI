from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from catalog.api.serializers import BookCreateSerializer, BookLinkSerializer, BookSerializer
from catalog.filters import BookFilter
from catalog.models import Book
from catalog.permissions import IsAdminOrAuthenticatedReadOnly
from common.mixins import AutoSchemaMixin


class BookAPIViewSet(AutoSchemaMixin, viewsets.ModelViewSet):
    """
    ViewSet для работы с книгами
    """
    queryset = Book.objects.all().prefetch_related('authors', 'genres')
    serializer_class = BookSerializer
    filterset_class = BookFilter
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'authors__name', 'genres__name']
    ordering_fields = ['name', 'authors__name', 'genres__name']
    tags = ['catalog/books']

    @action(methods=['get'], detail=True, serializer_class=BookLinkSerializer)
    def download(self, request, pk):
        """Получить ссылки на скачивание книги"""
        book = self.get_object()
        serialized_data = self.get_serializer(book.book_links.all(), many=True).data
        return Response(data={"book_links": serialized_data})

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return BookCreateSerializer
        return super().get_serializer_class()
