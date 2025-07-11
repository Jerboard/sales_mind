from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date, time
from sqlalchemy.dialects import postgresql as psql

import sqlalchemy as sa
import typing as t

from .base import Base, begin_connection


class PromptCategory(Base):
    __tablename__ = "prompt_categories"

    name: Mapped[str] = mapped_column(sa.String(255))
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    ordering: Mapped[int] = mapped_column(sa.Integer, default=1)

    @classmethod
    async def get_all(cls) -> t.Optional[list[t.Self]]:
        """Возвращает строку по id"""

        query = sa.select(cls).where(cls.is_active == True).order_by(cls.ordering)

        async with begin_connection() as conn:
            result = await conn.execute(query)

        return result.scalars().all()
