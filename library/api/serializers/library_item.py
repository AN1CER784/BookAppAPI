from rest_framework import serializers
from catalog.models import Book
from library.api.serializers.progress import ProgressSerializer
from library.models import LibraryItem


class LibraryItemBookSerializer(serializers.Serializer):
    """Вложенный сериалайзер для книги айтема библиотеки"""
    name = serializers.CharField(max_length=100)
    image = serializers.ImageField()


class LibraryItemSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели LibraryItem"""

    class Meta:
        model = LibraryItem
        fields = ['id', 'book_id', 'book', 'user', 'progress']
        read_only_fields = ('user',)

    book = LibraryItemBookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source='book',
        write_only=True
    )
    progress = ProgressSerializer(source='library_item_progress', read_only=True)
