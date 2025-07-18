from sqlalchemy.orm import Mapped, mapped_column, relationship, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy.dialects import postgresql as psql

import sqlalchemy as sa
import typing as t

from .base import Base, begin_connection
from settings import conf


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)

    full_name: Mapped[str] = mapped_column(sa.String)
    username: Mapped[str] = mapped_column(sa.String, nullable=True)
    email: Mapped[str] = mapped_column(sa.String, nullable=True)

    subscription_end: Mapped[datetime] = mapped_column(sa.DateTime, nullable=True)
    requests_remaining: Mapped[int] = mapped_column(sa.Integer, default=0)
    tariff_id: Mapped[int] = mapped_column(sa.ForeignKey("tariffs.id"), nullable=True)

    is_accepted: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    is_ban: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    is_used_trial: Mapped[bool] = mapped_column(sa.Boolean, default=False)

    tariff: Mapped["Tariff"] = relationship("Tariff", backref="user")

    def subscription_end_str(self) -> t.Optional[str]:
        if self.subscription_end:
            return self.subscription_end.strftime(conf.datetime_format)


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
    async def update(
            cls,
            user_id: int,
            add_requests: int = None,
            subscription_end: datetime = None,
            is_accepted: bool = None,
            is_used_trial: bool = None,
            email: str = None,
    ) -> None:
        """Обновляет данные"""
        now = datetime.now()
        query = sa.update(cls).where(cls.id == user_id).values(updated_at=now)

        if add_requests:
            query = query.values(requests_remaining=cls.requests_remaining + add_requests)

        if subscription_end:
            query = query.values(subscription_end=subscription_end)

        if email:
            query = query.values(email=email)

        if is_accepted is not None:
            query = query.values(is_accepted=is_accepted)

        if is_used_trial is not None:
            query = query.values(is_used_trial=is_used_trial)

        async with begin_connection() as conn:
            await conn.execute(query)
            await conn.commit()

    @classmethod
    async def get_full_user(cls, user_id: int) -> sa.select:
        query = sa.select(cls).options(joinedload(cls.tariff)).where(cls.id == user_id)
        async with begin_connection() as conn:
            result = await conn.execute(query)

        return result.scalars().first()
