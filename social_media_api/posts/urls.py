from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import SimpleRouter
from .views import PostViewSet, CommentViewSet, UserFeedView

router = routers.SimpleRouter()
router.register(r'posts', PostViewSet)
router.register('posts', PostViewSet)

posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
    path('feed/', UserFeedView.as_view(), name='user_feed'),
]