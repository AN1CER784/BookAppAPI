from rest_framework.routers import APIRootView

from BookAppAPI.custom_router import EnhancedAPIRouter
from catalog.api.views import BookAPIViewSet, AuthorAPIViewSet, GenreAPIViewSet


class CatalogAPIRootView(APIRootView):
    """Catalog view для апи."""

    __doc__ = 'Приложение каталога'
    name = 'catalog'


router = EnhancedAPIRouter()
router.APIRootView = CatalogAPIRootView

router.register(r"books", BookAPIViewSet, 'books')
router.register(r"authors", AuthorAPIViewSet, 'authors')
router.register(r"genres", GenreAPIViewSet, 'genres')
