from django.contrib import admin

from catalog.models import Book, Author, Genre


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'image')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'image')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'image')
