from rest_framework import serializers

from catalog.models import Book
from reviews.models import BookReview


class BookReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели BookReview"""
    class Meta:
        fields = ("id", "book_id", "user", "rating", "text", "likes_count", "dislikes_count", "book")
        model = BookReview
        read_only_fields = ('user',)

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source='book',
        write_only=True
    )
    book = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
