from django.db import models


class BaseCatalogClass(models.Model):
    """Абстрактная модель каталога"""
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, blank=True, null=True)
    image = models.ImageField(upload_to='catalog_images', blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name}"
