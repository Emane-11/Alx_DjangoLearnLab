
from django.urls import path
from .views import NotificationListView, NotificationMarkAsReadView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('notifications/<int:pk>/read/', NotificationMarkAsReadView.as_view(), name='notification_read'),
]
