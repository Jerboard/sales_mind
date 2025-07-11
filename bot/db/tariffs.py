import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

import typing as t
from .base import Base, begin_connection


class Tariff(Base):
    __tablename__ = "tariffs"

    name: Mapped[str] = mapped_column(sa.String(100))
    description: Mapped[str] = mapped_column(sa.Text)
    price: Mapped[float] = mapped_column(sa.Numeric(10, 2))
    duration: Mapped[int] = mapped_column(sa.Integer)
    response_count: Mapped[int] = mapped_column(sa.Integer)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)

    ordering: Mapped[int] = mapped_column(sa.Integer, default=1)

    def __repr__(self) -> str:
        return f"<Tariff id={self.id} name='{self.name}'>"

    @classmethod
    async def get_all(cls) -> t.Optional[list[t.Self]]:
        query = sa.select(cls).where(cls.is_active == True).order_by(cls.ordering)

        async with begin_connection() as conn:
            result = await conn.execute(query)

        return result.scalars().all()