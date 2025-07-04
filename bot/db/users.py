from sqlalchemy.orm import Mapped, mapped_column, relationship, joinedload
from datetime import datetime, date, time
from sqlalchemy.dialects import postgresql as psql

import sqlalchemy as sa
import typing as t

from .base import Base, begin_connection


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)

    full_name: Mapped[str] = mapped_column(sa.String)
    username: Mapped[str] = mapped_column(sa.String, nullable=True)
    subscription_end: Mapped[datetime] = mapped_column(sa.DateTime, nullable=True)
    requests_remaining: Mapped[int] = mapped_column(sa.Integer, default=False)

    is_accepted: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    is_ban: Mapped[bool] = mapped_column(sa.Boolean, default=False)

    @classmethod
    async def add(cls, user_id: int, full_name: str, username: str) -> None:
        """Добавляет новую запись в таблицу users"""
        now = datetime.now()
        query = (
            psql.insert(cls)
            .values(
                created_at=now,
                updated_at=now,
                id=user_id,
                full_name=full_name,
                username=username,
            ).on_conflict_do_update(
                index_elements=[cls.id],
                set_={"full_name": full_name, 'username': username, 'updated_at': now}
            )
        )

        async with begin_connection() as conn:
            result = await conn.execute(query)
            await conn.commit()
        return result.inserted_primary_key[0]

    @classmethod
    async def update(cls, user_id: int, is_accepted: bool = None) -> None:
        """Обновляет данные"""
        now = datetime.now()
        query = sa.update(cls).where(cls.id == user_id).values(updated_at=now)

        if is_accepted is not None:
            query = query.values(is_accepted=is_accepted)

        async with begin_connection() as conn:
            await conn.execute(query)
            await conn.commit()
