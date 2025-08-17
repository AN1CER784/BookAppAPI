from django.db import models

from catalog.models.base_catalog import BaseCatalogClass


class Book(BaseCatalogClass):
    """
    Модель книги пронаследованная от базового класса
    Связи:
    - Many-to-Many с Author (много книг - много авторов)
    - Many-to-Many с Genre (много книг - много жанров)
     """
    authors = models.ManyToManyField('Author', 'book')
    genres = models.ManyToManyField('Genre', 'book')


class BookLink(models.Model):
    """
    Модель ссылки на книгу для скачивания, содержит поле самой ссылки и внешний ключ на книгу
    Связи:
    - Many-to-Many с Author (много книг - много авторов)
    """
    link = models.URLField(max_length=100)
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name="book_links")
