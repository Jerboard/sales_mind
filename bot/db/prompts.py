from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date, time
from sqlalchemy.dialects import postgresql as psql

import sqlalchemy as sa
import typing as t

from .base import Base, begin_connection


class Prompt(Base):
    __tablename__ = "prompts"

    category_id: Mapped[int] = mapped_column(sa.ForeignKey("prompt_categories.id"))

    # id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
    # user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
    # created_at: Mapped[datetime] = mapped_column(sa.DateTime(), default=sa.func.now())

    name: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    model: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    hint: Mapped[str] = mapped_column(sa.Text, nullable=True)
    role: Mapped[str] = mapped_column(sa.Text, nullable=True)
    prompt: Mapped[str] = mapped_column(sa.Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)

    @classmethod
    async def get_prompt_category(cls, category_id: int) -> t.Optional[list[t.Self]]:
        """Возвращает промпты категории"""

        query = sa.select(cls).where(cls.category_id == category_id, cls.is_active == True)

        async with begin_connection() as conn:
            result = await conn.execute(query)

        return result.scalars().all()
