from rest_framework import serializers

from recommendations.models.recommendation import Recommendation


class RecommendationSerializer(serializers.ModelSerializer):
    """Сериалайзер рекомендации, выводит информацию о рекомендованных книгах"""
    book_name = serializers.CharField(source='book.name', read_only=True)
    book_image = serializers.ImageField(source='book.image', read_only=True)
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    class Meta:
        model = Recommendation
        fields = ('id', 'user', 'book_name', 'book_image', 'score', 'created_at')
        read_only_fields = fields