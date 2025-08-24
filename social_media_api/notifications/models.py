from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    """
    Model for notifications based on user interactions.
    """
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='acting_notifications')
    verb = models.CharField(max_length=20)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    # GenericForeignKey to link to any object (Ex: Post, Comment, User)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.actor.username} {self.verb} {self.target.__class__.__name__} for {self.recipient.username}'
