from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from reviews.models.base_message import BaseMessage


class BookReview(BaseMessage):
    """
    Модель обзора книги.

    Связи:
    - Many-to-One с Book (поле book) — книга, на которую написан обзор.
    - Наследует BaseMessage (поддерживает связь с пользователем и голосами).

    Дополнительно:
    - Рейтинг от 1 до 10.
    """
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    book = models.ForeignKey('catalog.Book', on_delete=models.CASCADE, related_name="book_reviews")