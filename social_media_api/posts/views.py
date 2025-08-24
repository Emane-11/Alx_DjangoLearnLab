from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework import generics


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        # This ensures comments are specific to a post
        return self.queryset.filter(post_id=self.kwargs['post_pk'])

    def perform_create(self, serializer):
        # Pass the post to the serializer context
        post = Post.objects.get(pk=self.kwargs['post_pk'])
        serializer.save(author=self.request.user, post=post)

class UserFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the list of users the current user is following
        followed_users = self.request.user.following.all()
        # Return posts from those users, ordered by creation date
        return Post.objects.filter(author__in=followed_users).order_by('-created_at')