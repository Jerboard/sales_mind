from uuid import uuid4

from init import client_redis
from settings import conf


async def get_or_create_session(user_id: int) -> str:
    key = f"session:{user_id}"
    session_id = await client_redis.get(key)

    if not session_id:
        # Нет сессии — создаём новую
        session_id = str(uuid4())
        await client_redis.set(key, session_id, ex=conf.session_ttl)
    else:
        # Сессия есть — продлеваем время жизни
        await client_redis.expire(key, conf.session_ttl)

    return session_id

