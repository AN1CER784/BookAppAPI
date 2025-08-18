from django.contrib import admin

from reviews.models import Reply, BookReview


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    fields = ('text', 'content_type', 'object_id', 'votes', 'user')


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    fields = ('text', 'book', 'rating', 'votes', 'user')
