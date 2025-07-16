from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status, permissions
from yookassa.domain.notification import WebhookNotification
from datetime import datetime, timedelta, timezone
from apscheduler.triggers.date import DateTrigger
import logging

import bot_admin.utils as ut
from .models import LogsUser, Payment, User, Tariff, Request, Text
from web.settings import bot, scheduler
from enums import PayType, HandlerKey

logger = logging.getLogger(__name__)


class AdminStatsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        stats = LogsUser()  # создаём «сервисный» экземпляр

        paid_users_count = Payment.get_unique_users()

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
            "percent_subscribers": f"{round(paid_users_count / all_users_count * 100, 2)}%",
            "top_commands": stats.get_top_actions(),
        }
        return Response(data)


# приём платежей
class YooKassaWebhookView(APIView):
    permission_classes = [permissions.AllowAny]  # уведомления приходят от внешнего сервиса

    def post(self, request):
        try:
            notification = WebhookNotification(request.data)

            # 3) Достаем данные
            event_type = notification.event  # например, 'payment.succeeded'
            payment_object = notification.object  # это экземпляр domain-модели Payment
            payment_id = payment_object.id  # ID платежа
            amount = payment_object.amount.value
            status_ = payment_object.status  # например, 'succeeded'
            metadata = payment_object.metadata

            if status_ == 'succeeded':
                user_id = int(metadata.get('user_id'))
                tariff_id = int(metadata.get('tariff_id'))
                payment_type = metadata.get('pay_type')
                session_id = metadata.get('session_id')

                Payment.add(
                    user_id=user_id,
                    tariff_id=tariff_id,
                    amount=amount,
                    payment_id=payment_id,
                    payment_type=payment_type
                )
                user = User.get_user(user_id)

                if payment_type == PayType.TARIFF.value:
                    tariff = Tariff.get_by_id(tariff_id)
                    subscription_end = (user.subscription_end + timedelta(days=tariff.duration)).replace(tzinfo=None)

                    User.update(
                        user_id=user_id,
                        add_requests=tariff.response_count,
                        subscription_end=subscription_end,
                        tariff_id=tariff_id
                    )

                    subscription_end = datetime.now(timezone.utc)
                    scheduler.add_job(
                        func=ut.send_notice,
                        args=[user_id, HandlerKey.SEND_NOTICE_1.key],
                        trigger=DateTrigger(run_date=subscription_end - timedelta(days=2)),
                        # trigger=DateTrigger(run_date=subscription_end + timedelta(seconds=10)),
                        id=f'{HandlerKey.SEND_NOTICE_1.value}-{user_id}',
                        replace_existing=True
                    )

                    scheduler.add_job(
                        func=ut.send_notice,
                        args=[user_id, HandlerKey.SEND_NOTICE_2.key],
                        trigger=DateTrigger(run_date=subscription_end),
                        # trigger=DateTrigger(run_date=subscription_end + timedelta(seconds=10)),
                        id=f'{HandlerKey.SEND_NOTICE_2.value}-{user_id}',
                        replace_existing=True
                    )

                else:
                    tariff = Request.get_by_id(tariff_id)
                    User.update(user_id=user_id, add_requests=tariff.response_count)

                text = Text.get_by_key(HandlerKey.PAYMENT_SUCCESS.key)
                bot.send_message(chat_id=user_id, text=text.text, reply_markup=ut.get_success_pay_kb())

                # сохраняем действия пользователя
                LogsUser.add(
                    user_id=user.id,
                    action=HandlerKey.PAYMENT_SUCCESS.key,
                    comment=payment_type,
                    session=session_id
                )

            return Response(
                {
                    "received": True,
                    "payment_id": payment_id,
                    "status": status_,
                    "metadata": metadata,
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.warning(e, exc_info=True)
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
