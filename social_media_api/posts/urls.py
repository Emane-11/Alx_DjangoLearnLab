from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PostViewSet, CommentViewSet, UserFeedView, like_post, unlike_post

router = SimpleRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)
# Register the UserFeedView with the router to automatically generate its URL patterns.
router.register('feed', UserFeedView)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:pk>/like/', like_post, name='like_post'),
    path('posts/<int:pk>/unlike/', unlike_post, name='unlike_post'),
]
