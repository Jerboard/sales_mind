from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

import logging

from .models import LogsUser

logger = logging.getLogger(__name__)

# your_app/views.py


class AdminStatsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        stats = LogsUser()  # создаём «сервисный» экземпляр

        multisession_users_count = stats.get_users_with_multiple_sessions()
        msg_count = stats.get_total_messages()

        all_users_count = stats.get_unique_users()
        active_users_count = stats.get_unique_users('active')

        data = {
            "active_day": stats.get_unique_users('day'),
            "active_week": stats.get_unique_users('week'),
            "active_month": stats.get_unique_users('month'),
            "sessions_gt1": multisession_users_count,
            "return_rate": f"{round(multisession_users_count / all_users_count * 100, 2)}%",
            "messages_total": msg_count,
            "messages_avg": stats.get_avg_messages_per_session(msg_count),
            "percent_active": f"{round(active_users_count / all_users_count * 100, 2)}%",
            "percent_subscribers": f"?%",
            "top_commands": stats.get_top_actions(),
        }
        return Response(data)

