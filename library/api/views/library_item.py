

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from common.mixins import AutoSchemaMixin
from library.models import LibraryItem, Progress
from library.api.serializers import LibraryItemSerializer, ProgressSerializer


class LibraryItemViewSet(AutoSchemaMixin, viewsets.ModelViewSet):
    """
    ViewSet для работы с айтемами библиотеки
    """
    queryset = LibraryItem.objects.all()
    serializer_class = LibraryItemSerializer
    permission_classes = (permissions.IsAuthenticated,)
    tags = ['library/books']

    def get_queryset(self):
        return LibraryItem.objects.filter(user=self.request.user).select_related('library_item_progress', 'book')

    def perform_create(self, serializer):
        lib_item = serializer.save(user=self.request.user)
        Progress.objects.create(library_item=lib_item)

    @action(methods=["get", "patch"], detail=True, serializer_class=ProgressSerializer)
    def progress(self, request, pk):
        """Узнать или изменить прогресс айтема библиотеки"""
        instance = self.get_object()
        if request.method == "GET":
            serializer = self.get_serializer(instance.library_item_progress)
            return Response(serializer.data)
        serializer = self.get_serializer(instance.library_item_progress, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['get'], detail=False, serializer_class=LibraryItemSerializer)
    def active_items(self, request):
        """Получить активные айтемы библиотеки (книги, которые сейчас читает пользователь)"""
        queryset = self.get_queryset().filter(user=request.user).filter(library_item_progress__complete_percentage__lt=100)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, serializer_class=LibraryItemSerializer)
    def done_items(self, request):
        """Получить завершенные айтемы библиотеки (книги, которые прочитал пользователь)"""
        queryset = self.get_queryset().filter(user=request.user).filter(library_item_progress__complete_percentage=100)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
