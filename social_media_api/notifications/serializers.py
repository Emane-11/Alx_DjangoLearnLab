from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserSerializer 
from posts.serializers import PostSerializer  

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target', 'read', 'timestamp']
        read_only_fields = ['id', 'recipient', 'actor', 'verb', 'target', 'timestamp']

    def get_target(self, obj):
        if obj.target:
            if isinstance(obj.target, obj.target.__class__):
                if obj.content_type.model == 'post':
                    return PostSerializer(obj.target).data
                # Add other cases for other models (e.g., 'comment') as needed
                # elif obj.content_type.model == 'comment':
                #     return CommentSerializer(obj.target).data
        return None