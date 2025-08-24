from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db import transaction

from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]
    pagination_class = PostPagination

    def get_queryset(self):
        """
        Get posts from followed users, or all posts if no users are followed.
        """
        user = self.request.user
        followed_users = user.following.all()
        if followed_users.exists():
            return Post.objects.filter(author__in=followed_users).order_by('-created_at')
        return Post.objects.all().order_by('-created_at')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    
    # Check if the user has already liked the post
    if Like.objects.filter(post=post, user=user).exists():
        return Response({"detail": "Post already liked."}, status=status.HTTP_409_CONFLICT)
        
    Like.objects.create(post=post, user=user)

    # Create a notification for the post author
    if user != post.author:
        Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb='liked',
            content_type=ContentType.objects.get_for_model(Post),
            object_id=post.id,
            target=post
        )

    return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    
    try:
        like = Like.objects.get(post=post, user=user)
        like.delete()
        
        # Remove the notification as well
        if user != post.author:
            Notification.objects.filter(
                recipient=post.author,
                actor=user,
                verb='liked',
                content_type=ContentType.objects.get_for_model(Post),
                object_id=post.id
            ).delete()

        return Response({"detail": "Post unliked successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Like.DoesNotExist:
        return Response({"detail": "Post was not liked by this user."}, status=status.HTTP_404_NOT_FOUND)

