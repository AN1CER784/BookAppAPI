from rest_framework.routers import APIRootView

from BookAppAPI.custom_router import EnhancedAPIRouter
from library.api.views import LibraryItemViewSet


class LibraryAPIRootView(APIRootView):
    """Library view для апи."""

    __doc__ = 'Приложение библиотеки'
    name = 'library'


router = EnhancedAPIRouter()
router.APIRootView = LibraryAPIRootView

router.register("books", LibraryItemViewSet, 'books')