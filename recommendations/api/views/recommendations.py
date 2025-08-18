from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from recommendations.api.serializers import RecommendationSerializer
from recommendations.models.recommendation import Recommendation


class RecommendationAPIViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Recommendation.objects.filter(user=self.request.user).order_by('-score').select_related('user', 'book')
