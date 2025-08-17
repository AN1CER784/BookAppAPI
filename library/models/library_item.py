from django.db import models


class LibraryItem(models.Model):
    """
    Модель айтема библиотеки пользователя
    Связи:
    - One-to-One с Book (один айтем - одна книга )
    - Many-to-One с User (много айтемов - один пользователь)
     """
    book = models.OneToOneField(to="catalog.Book", on_delete=models.CASCADE)
    user = models.ForeignKey(to="auth.User", on_delete=models.CASCADE)

    class Meta:
        ordering = ['-library_item_progress__updated_at']
