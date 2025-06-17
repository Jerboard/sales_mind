from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date, time
from sqlalchemy.dialects import postgresql as psql

import sqlalchemy as sa
import typing as t

from .base import Base, begin_connection


import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Message(Base):
    __tablename__ = "messages"

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
    prompt_id: Mapped[int] = mapped_column(sa.ForeignKey("prompts.id"))

    request: Mapped[str] = mapped_column(sa.Text)
    response: Mapped[str] = mapped_column(sa.Text)
    time_answer: Mapped[str] = mapped_column(sa.String(255))

    prompt_tokens: Mapped[int] = mapped_column(sa.Integer)
    completion_tokens: Mapped[int] = mapped_column(sa.Integer)

    is_like: Mapped[bool] = mapped_column(sa.Boolean, nullable=True)

    # prompt: Mapped["Prompt"] = relationship(back_populates="messages")
    # user: Mapped["User"] = relationship(back_populates="messages")


    def __repr__(self) -> str:
        return f"<Message id={self.id} user_id={self.user_id}>"

    @classmethod
    async def add(
            cls,
            user_id: int,
            prompt_id: int,
            request: str,
            response: str,
            time_answer: str,
            prompt_tokens: int,
            completion_tokens: int,
    ) -> int:
        """
        Создаёт и сохраняет запись Message.
        Возвращает уже обновлённый объект.
        """
        query = sa.insert(cls).values(
            user_id=user_id,
            prompt_id=prompt_id,
            request=request,
            response=response,
            time_answer=time_answer,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
        )

        async with begin_connection() as conn:
            result = await conn.execute(query)
            await conn.commit()
        return result.inserted_primary_key[0]

    @classmethod
    async def update(
            cls,
            message_id: int,
            is_like: bool = None,
    ) -> None:

        query = sa.update(cls).where(cls.id == message_id)

        if is_like is not None:
            query = query.values(is_like=is_like)

        async with begin_connection() as conn:
            result = await conn.execute(query)
            await conn.commit()

    @classmethod
    async def get_user_history(
            cls,
            user_id: int,
            prompt_id: int,
            limit: int = 10,
    ) -> list[t.Self]:

        query = sa.select(cls).where(cls.user_id == user_id, cls.prompt_id == prompt_id).limit(limit)

        async with begin_connection() as conn:
            result = await conn.execute(query)

        return result.scalars().all()
