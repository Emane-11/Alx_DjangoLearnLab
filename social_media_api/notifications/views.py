from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    """
    API view to list all notifications for the authenticated user.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter notifications for the current user and order them by newest first
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')

class NotificationMarkAsReadView(generics.UpdateAPIView):
    """
    API view to mark a specific notification as read.
    """
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.read = True
        instance.save()
        return Response({"detail": "Notification marked as read."}, status=status.HTTP_200_OK)