from rest_framework import serializers

from library.models import Progress


class ProgressSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Progress"""
    class Meta:
        model = Progress
        fields = ['complete_percentage']
