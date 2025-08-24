from rest_framework import serializers
from .models import Post, Comment, Like
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the user model, to display author information.
    """
    class Meta:
        model = User
        fields = ['username', 'email'] 

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating a Post.
    """
    class Meta:
        model = Post
        fields = ['id', 'content', 'created_at']
        read_only_fields = ['author']

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating a Comment.
    """
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at']
        read_only_fields = ['author']

class PostListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing posts with additional information like like count and
    whether the current user has liked the post.
    """
    like_count = serializers.IntegerField(read_only=True)
    author = AuthorSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'like_count', 'is_liked']

    def get_is_liked(self, obj):
        """
        Check if the request user has liked the post.
        """
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return Like.objects.filter(post=obj, user=request.user).exists()
        return False
    

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Like
        fields = ['user', 'post']