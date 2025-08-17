from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Progress(models.Model):
    """
    Модель прогресса
    Связи:
    - One-to-One с LibraryItem (один прогресс - один айтем)
     """
    complete_percentage = models.IntegerField(default=0,
                                              validators=[MinValueValidator(0), MaxValueValidator(100)]
                                              )
    library_item = models.OneToOneField(to="LibraryItem", on_delete=models.CASCADE, related_name="library_item_progress")
    updated_at = models.DateTimeField(auto_now=True)
