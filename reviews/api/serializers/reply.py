from rest_framework import serializers

from reviews.models import BookReview, Reply


class ReplySerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Reply"""
    class Meta:
        fields = ("id", "user", "text", "likes_count", "dislikes_count", 'object_id', 'content_type', 'review_id')
        read_only_fields = ('object_id', 'content_type')
        model = Reply

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)
    review_id = serializers.PrimaryKeyRelatedField(
        queryset=BookReview.objects.all(),
        source='review',
        write_only=True
    )
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        read_only=True,
    )
