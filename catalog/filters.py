from django_filters import FilterSet

from catalog.models import Book


class BookFilter(FilterSet):
    class Meta:
        model = Book
        fields = {
            'authors__name': ['iexact'],
            'genres__name': ['iexact']
        }
