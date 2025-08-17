from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class BaseMessageQuerySet(models.QuerySet):
    def with_votes(self):
        """Аннотирование сообщений количеством лайков и дизлайков на них"""
        reviews_with_votes = self.annotate(
            likes_count=
            models.Count('votes', filter=models.Q(votes__value=1)),
            dislikes_count=
            models.Count('votes', filter=models.Q(votes__value=-1))
        ).order_by('-likes_count', '-dislikes_count')
        return reviews_with_votes


class BaseMessage(models.Model):
    """
    Абстрактная модель сообщения
    Связи:
    Many-to-One с User (много сообщений - один пользователь)
    GenericRelation с Vote (голоса могут быть привязаны к разным объектам).
    """
    user = models.ForeignKey('auth.User', on_delete=models.SET_DEFAULT, default=None)
    text = models.TextField()
    votes = GenericRelation(
        'reviews.Vote',
        content_type_field='content_type',
        object_id_field='object_id',
        related_query_name='votes'
    )

    objects = BaseMessageQuerySet.as_manager()

    class Meta:
        abstract = True
