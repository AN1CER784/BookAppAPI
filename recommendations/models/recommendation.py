from django.db import models


class Recommendation(models.Model):
    """
    Модель рекомендации
    Связи:
    - Many-to-One с User (много рекомендаций - один пользователь)
    - Many-to-One с Book (много рекомендаций - одна книга)
     """
    user = models.ForeignKey('auth.User', related_name='recommendations', on_delete=models.CASCADE)
    book = models.OneToOneField('catalog.Book', related_name='recommendations', on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
