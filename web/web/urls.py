from django.contrib import admin
from django.urls import path

from bot_admin.views import AdminStatsAPIView, YooKassaWebhookView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/admin_stats', AdminStatsAPIView.as_view(), name='admin-stats'),
    path('api/payment', YooKassaWebhookView.as_view(), name='payment'),
]
