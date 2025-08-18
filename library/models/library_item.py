from django.db import models


class LibraryItem(models.Model):
    """
    Модель айтема библиотеки пользователя
    Связи:
    - One-to-One с Book (один айтем - одна книга )
    - Many-to-One с User (много айтемов - один пользователь)
     """
    book = models.ForeignKey(to="catalog.Book", on_delete=models.CASCADE, related_name='library_item')
    user = models.ForeignKey(to="auth.User", on_delete=models.CASCADE, related_name='library_item')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-library_item_progress__updated_at']
        unique_together = ('book', 'user')