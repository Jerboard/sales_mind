from datetime import timedelta, datetime
from sqlalchemy.ext.asyncio import AsyncSession

import asyncio

import db
from db.base import begin_connection
import keyboards as kb
from celery import Celery, shared_task
from settings import conf, log_error
from init import bot, ENGINE
from enums import HandlerKey, PayType


celery_app = Celery(
    conf.celery_project,
    broker=f"redis://{conf.redis_host}:{conf.redis_port}/0",
    backend=f"redis://{conf.redis_host}:{conf.redis_port}/1"
)


# дставим тариф добавляем время и всё такое
@shared_task
async def send_success_payment(user_id: int, tariff_id: int, pay_type: str, session_id: str):
    # async def inner():
        async with AsyncSession(ENGINE, expire_on_commit=False) as session:

            user = await db.User.get_by_id_celery(entry_id=user_id, session=session)
            text = await db.Text.get_text(HandlerKey.PAYMENT_SUCCESS.key)
            # сохраняем действия пользователя
            await db.LogsUser.add(
                user_id=user.id,
                action=HandlerKey.PAYMENT_SUCCESS.key,
                comment=pay_type,
                session=session_id
            )

        if pay_type == PayType.TARIFF.value:
            async with AsyncSession(ENGINE, expire_on_commit=False) as session:
                tariff = await db.Tariff.get_by_id_celery(session=session, entry_id=tariff_id)
                subscription_end = (user.subscription_end + timedelta(days=tariff.duration)).replace(tzinfo=None)

                await db.User.update_celery(
                    session=session,
                    user_id=user_id,
                    add_requests=tariff.response_count,
                    subscription_end=subscription_end
                )

            # первое напоминание
            send_notice.apply_async(
                args=[user_id, HandlerKey.SEND_NOTICE_1.value],
                eta=subscription_end - timedelta(days=2)
            )

            # # второе напоминание
            send_notice.apply_async(
                args=[user_id, HandlerKey.SEND_NOTICE_2.value],
                eta=subscription_end
            )

        else:
            async with AsyncSession(ENGINE, expire_on_commit=False) as session:
                tariff = await db.Request.get_by_id_celery(session=session, entry_id=tariff_id)
                await db.User.update_celery(session=session, user_id=user_id, add_requests=tariff.response_count)

        await bot.send_message(chat_id=user_id, text=text, reply_markup=kb.get_success_pay_kb())
        await bot.session.close()

    # asyncio.run(inner())


# дставим тариф добавляем время и всё такое
# @celery_app.task
@shared_task
def send_notice(user_id: int, text: str):
    async def notice():
        try:
            # text = await db.Text.get_text(key)

            await bot.send_message(chat_id=user_id, text=text, reply_markup=kb.get_start_payment_kb())
            await bot.session.close()

            # сохраняем действия пользователя
            # await db.LogsUser.add(
            #     user_id=user_id,
            #     action=key,
            # )
        except Exception as e:
            log_error(e)

    asyncio.run(notice())
