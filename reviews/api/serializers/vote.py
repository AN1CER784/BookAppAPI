from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Vote


class VoteValueField(serializers.ChoiceField):
    """Field для поля value голоса"""
    def __init__(self, **kwargs):
        """Инициализируем choices поля value и создаем коллекции для методов to_representation и to_internal_value"""
        choices = Vote.VOTE_CHOICES
        super().__init__(choices=choices, **kwargs)
        self._label_to_key = {label.upper(): key for key, label in choices}
        self._valid_keys = {key for key, _ in choices}

    def to_representation(self, value):
        """Получаем LIKE ИЛИ DISLIKE для удобного отображения клиенту"""
        return dict(self.choices).get(value)

    def to_internal_value(self, data):
        """Приводим к значению необходимому базе данных 1 или -1"""
        if data is None:
            self.fail('invalid_choice', input=data)

        if isinstance(data, int):
            if data in self._valid_keys:
                return data
            self.fail('invalid_choice', input=data)

        if isinstance(data, str):
            s = data.strip().upper()
            try:
                num = int(s)
                if num in self._valid_keys:
                    return num
            except ValueError:
                pass
            key = self._label_to_key.get(s.upper())
            if key is not None:
                return key
        self.fail('invalid_choice', input=data)


class VoteSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Vote"""
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        read_only=True,
    )
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    value = VoteValueField()

    class Meta:
        model = Vote
        fields = ('id', 'value', 'user', 'object_id', 'content_type')
        read_only_fields = ('user', 'content_type', 'object_id')

    def create(self, validated_data):
        user = self.context['request'].user
        content_type = validated_data['content_type']
        object_id = validated_data['object_id']
        value = validated_data['value']
        vote, created = Vote.objects.get_or_create(
            user=user,
            content_type=content_type,
            object_id=object_id,
            defaults={'value': value}
        )
        if not created:
            raise ValidationError("You have already voted for this review.")
        return vote
