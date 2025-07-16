from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date, time
from sqlalchemy.dialects import postgresql as psql

import sqlalchemy as sa
import typing as t

from .base import Base, begin_connection


class DisallowCategory(Base):
    __tablename__ = "disallow_categories"

    tariff_id: Mapped[int] = mapped_column(sa.ForeignKey("tariffs.id"))
    category_id: Mapped[int] = mapped_column(sa.ForeignKey("prompt_categories.id"))

    @classmethod
    async def get_disallow_list(cls, tariff_id) -> list[int]:
        query = sa.select(cls).where(cls.tariff_id == tariff_id)

        async with begin_connection() as conn:
            results = await conn.execute(query)

        return [result.category_id for result in results.scalars().all()]
