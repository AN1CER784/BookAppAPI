from django.contrib import admin

from recommendations.models.recommendation import Recommendation


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    fields = ('user', 'book', 'score', 'created_at')