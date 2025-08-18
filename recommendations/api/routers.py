from rest_framework.routers import APIRootView

from BookAppAPI.custom_router import EnhancedAPIRouter
from recommendations.api.views.recommendations import RecommendationAPIViewSet


class RecommendationsAPIRootView(APIRootView):
    """Корневой view для апи."""

    __doc__ = 'Приложение recommendations'
    name = 'recommendations'


router = EnhancedAPIRouter()
router.APIRootView = RecommendationsAPIRootView

router.register("user-recommendations", RecommendationAPIViewSet, 'user-recommendations')
