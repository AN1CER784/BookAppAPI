from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Vote(models.Model):
    """
    Модель голосования (лайк/дизлайк).

    Связи:
    - Many-to-One с User (один пользователь может оставить много голосов).
    - GenericForeignKey (content_object) — связь с любым объектом в базе,
      который поддерживает голосование.

    Ограничения:
    - Уникальность голоса: один пользователь может проголосовать только один раз
      за конкретный объект (см. unique_together).
    """
    LIKE = 1
    DISLIKE = -1

    VOTE_CHOICES = (
        (LIKE, "LIKE"),
        (DISLIKE, "DISLIKE"),
    )
    user = models.ForeignKey('auth.User', on_delete=models.SET_DEFAULT, default=None)
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
