from django.contrib import admin

from library.models import LibraryItem, Progress


class ProgressInline(admin.TabularInline):
    model = Progress
    extra = 1


@admin.register(LibraryItem)
class LibraryItemAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "user",)
    inlines = [ProgressInline]
