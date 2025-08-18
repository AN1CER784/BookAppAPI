from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from common.mixins import AutoSchemaMixin
from recommendations.api.serializers import RecommendationSerializer
from recommendations.models.recommendation import Recommendation


class RecommendationAPIViewSet(AutoSchemaMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = (IsAuthenticated,)
    tags = ['recommendations/user-recommendations']

    def get_queryset(self):
        return Recommendation.objects.filter(user=self.request.user).order_by('-score').select_related('user', 'book')
