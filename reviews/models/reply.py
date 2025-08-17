from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from reviews.models.base_message import BaseMessage


class Reply(BaseMessage):
    """
    Модель ответа.

    Связи:
    - Many-to-One с BookReview (поле review) — основной обзор, к которому относится ответ.
    - GenericForeignKey (content_object) — возможность привязки ответа к любому объекту.
    """
    review = models.ForeignKey('reviews.BookReview', on_delete=models.CASCADE, related_name="replies")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
