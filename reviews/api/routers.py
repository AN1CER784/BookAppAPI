from rest_framework.routers import APIRootView
from rest_framework_nested.routers import NestedSimpleRouter

from BookAppAPI.custom_router import EnhancedAPIRouter
from reviews.api.views import ReviewViewSet, ReplyViewSet, ReviewVoteViewSet, ReplyVoteViewSet


class ReviewsAPIRootView(APIRootView):
    """Корневой view для апи."""

    __doc__ = 'Приложение reviews'
    name = 'reviews'


router = EnhancedAPIRouter()
router.APIRootView = ReviewsAPIRootView

router.register(r"reviews", ReviewViewSet, 'reviews')

replies_router = NestedSimpleRouter(router, r'reviews', lookup='review')
replies_router.register(r'replies', ReplyViewSet, basename='review-replies')

reply_to_reply_router = NestedSimpleRouter(replies_router, r'replies', lookup='reply')
reply_to_reply_router.register(r'replies', ReplyViewSet, basename='reply-replies')

review_votes_router = NestedSimpleRouter(router, r'reviews', lookup='review')
review_votes_router.register(r'votes', ReviewVoteViewSet, basename='review-votes')

reply_votes_router = NestedSimpleRouter(replies_router, r'replies', lookup='parent_reply')
reply_votes_router.register(r'votes', ReplyVoteViewSet, basename='reply-votes')

reply_to_reply_votes_router = NestedSimpleRouter(reply_to_reply_router, r'replies', lookup='child_reply')
reply_to_reply_votes_router.register(r'votes', ReplyVoteViewSet, basename='reply-to-reply-votes')


router.register('', replies_router, 'nested_replies')
router.register('', reply_to_reply_router, 'nested_reply_to_reply')
router.register('', review_votes_router, 'nested_review_votes')
router.register('', reply_votes_router, 'nested_reply_votes')
router.register('', reply_to_reply_votes_router, 'nested_reply_to_reply_votes')