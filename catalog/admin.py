from django.contrib import admin

from catalog.models import Book, Author, Genre


class AuthorInline(admin.TabularInline):
    model = Book.authors.through
    extra = 1


class GenreInline(admin.TabularInline):
    model = Book.genres.through
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'image')
    inlines = [AuthorInline, GenreInline]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'image')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'image')
