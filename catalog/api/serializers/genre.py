from rest_framework import serializers

from catalog.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер объекта модели Жанр"""
    class Meta:
        model = Genre
        fields = ('name', 'description', 'image')
