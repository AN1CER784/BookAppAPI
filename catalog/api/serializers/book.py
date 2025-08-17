from django.db import transaction
from rest_framework import serializers
from rest_framework.reverse import reverse

from catalog.models import Book, Author, BookLink, Genre


class BookLinkSerializer(serializers.Serializer):
    """Вложенный сериалайзер для ссылок на скачивание книги"""
    link = serializers.URLField(max_length=100)


class AuthorBookSerializer(serializers.Serializer):
    """Вложенный сериалайзер для авторов книги"""
    name = serializers.CharField(max_length=100)


class GenreBookSerializer(serializers.Serializer):
    """Вложенный сериалайзер для жанров книги"""
    name = serializers.CharField(max_length=100)


class BookCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания и обновления объектов модели Book"""
    class Meta:
        model = Book
        fields = ('name', 'description', 'authors', 'genres', 'book_links')

    authors = AuthorBookSerializer(
        many=True,
    )
    genres = GenreBookSerializer(
        many=True,
    )
    book_links = BookLinkSerializer(
        many=True,
    )

    @staticmethod
    def _set_related(instance, authors=None, genres=None, book_links=None):
        if authors is not None:
            instance.authors.clear()
            for author in authors:
                author_obj, _ = Author.objects.get_or_create(**author)
                instance.authors.add(author_obj)

        if genres is not None:
            instance.genres.clear()
            for genre in genres:
                genre_obj, _ = Genre.objects.get_or_create(**genre)
                instance.genres.add(genre_obj)

        if book_links is not None:
            BookLink.objects.filter(book_id=instance.id).delete()
            for book_link in book_links:
                BookLink.objects.create(book=instance, **book_link)

    def create(self, validated_data):
        authors = validated_data.pop('authors', [])
        genres = validated_data.pop('genres', [])
        book_links = validated_data.pop('book_links', [])

        with transaction.atomic():
            book, created = Book.objects.get_or_create(**validated_data)
            if created:
                self._set_related(book, authors, genres, book_links)
        return book

    def update(self, instance, validated_data):
        authors = validated_data.pop('authors', None)
        genres = validated_data.pop('genres', None)
        book_links = validated_data.pop('book_links', None)

        with transaction.atomic():
            instance = super().update(instance, validated_data)
            self._set_related(instance, authors, genres, book_links)
        return instance


class BookSerializer(serializers.ModelSerializer):
    """Сериалайзер для чтения данных об объекте модели Book"""
    class Meta:
        model = Book
        fields = ('id', 'name', 'description', 'authors', 'genres', 'book_links')

    authors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
    )
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
    )
    book_links = serializers.SerializerMethodField()

    def get_book_links(self, obj):
        request = self.context.get('request')
        return reverse('catalog:books-download', kwargs={'pk': obj.pk}, request=request)
