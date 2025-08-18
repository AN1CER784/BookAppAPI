from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from recommendations.user_recommendation_service import RecommendationService

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates recommendations'

    def handle(self, *args, **options):
        for user in User.objects.iterator():
            RecommendationService(user=user).add_recommendations()
