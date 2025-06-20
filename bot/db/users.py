from sqlalchemy.orm import Mapped, mapped_column, relationship, joinedload
from datetime import datetime, date, time
from sqlalchemy.dialects import postgresql as psql

import sqlalchemy as sa
import typing as t

from .base import Base, begin_connection


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)

    # user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
    # created_at: Mapped[datetime] = mapped_column(sa.DateTime(), default=sa.func.now())
    full_name: Mapped[str] = mapped_column(sa.String)
    username: Mapped[str] = mapped_column(sa.String, nullable=True)
    subscription_end: Mapped[datetime] = mapped_column(sa.DateTime, nullable=True)

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
