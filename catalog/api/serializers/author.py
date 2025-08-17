from rest_framework import serializers

from catalog.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Автор"""
    class Meta:
        model = Author
        fields = ('name', 'description', 'image')
