from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date, time
from sqlalchemy.dialects import postgresql as psql

import sqlalchemy as sa
import typing as t

from .base import Base, begin_connection


class LogsUser(Base):
    __tablename__ = "logs_users"

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(sa.String)
    comment: Mapped[str] = mapped_column(sa.Text, nullable=True)
    session: Mapped[str] = mapped_column(sa.String, nullable=True)
    msg_id: Mapped[int] = mapped_column(sa.ForeignKey("messages.id"), nullable=True)

    @classmethod
    async def add(cls, user_id: int, action: str, session: str = None, comment: str = None, msg_id: int = None) -> None:
        query = sa.insert(cls).values(user_id=user_id, action=action, session=session)

        if comment:
            query = query.values(comment=comment)
        if msg_id:
            query = query.values(msg_id=msg_id)

        async with begin_connection() as conn:
            await conn.execute(query)
            await conn.commit()
