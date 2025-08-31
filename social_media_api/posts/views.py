from rest_framework import viewsets, mixins, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db import transaction

from .models import Post, Comment, Like
from .serializers import (
    PostSerializer,
    CommentSerializer,
    PostListSerializer,
)

# A custom paginator for the user feed to control the number of posts per page.
class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    A ViewSet for managing post-related actions.
    It supports creating, retrieving, updating, and deleting posts.
    """
    queryset = Post.objects.all().annotate(like_count=Count('likes'))
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        """
        Set the author of the post to the current authenticated user.
        """
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['GET'])
    def list_posts(self, request):
        """
        List all posts with a count of their likes.
        """
        queryset = self.get_queryset().order_by('-created_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PostListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = PostListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing comments on a post.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Set the author of the comment to the current authenticated user.
        """
        serializer.save(author=self.request.user)


class UserFeedView(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for the user's feed, showing posts from users they follow.
    """
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PostPagination

    def get_queryset(self):
        """
        Get posts from followed users, ordered by creation date.
        """
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    """
    Allow a user to like a post.
    """
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    with transaction.atomic():
        like, created = Like.objects.get_or_create(user=user, post=post)
        if created:
            return Response(
                {"detail": "Post liked successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"detail": "You have already liked this post."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    """
    Allow a user to unlike a post.
    """
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    with transaction.atomic():
        deleted, _ = Like.objects.filter(post=post, user=user).delete()
        if deleted:
            return Response(
                {"detail": "Post unliked successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "You have not liked this post."},
            status=status.HTTP_400_BAD_REQUEST,
        )
