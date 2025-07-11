from sqlalchemy.orm import Mapped, mapped_column, joinedload, relationship
from datetime import datetime, date, time
from sqlalchemy.dialects import postgresql as psql

import sqlalchemy as sa
import typing as t

from .base import Base, begin_connection


class Prompt(Base):
    __tablename__ = "prompts"

    category_id: Mapped[int] = mapped_column(sa.ForeignKey("prompt_categories.id"))

    name: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    model: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    hint: Mapped[str] = mapped_column(sa.Text, nullable=True)
    role: Mapped[str] = mapped_column(sa.Text, nullable=True)
    prompt: Mapped[str] = mapped_column(sa.Text, nullable=True)
    temperature: Mapped[float] = mapped_column(sa.Float, default=0.9)
    presence_penalty: Mapped[float] = mapped_column(sa.Float, default=0.4)
    frequency_penalty: Mapped[float] = mapped_column(sa.Float, default=0.3)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    ordering: Mapped[int] = mapped_column(sa.Integer, default=1)

    prompt_category: Mapped["PromptCategory"] = relationship("PromptCategory", backref="prompt")

    @classmethod
    async def get_prompt_category(cls, category_id: int) -> t.Optional[list[t.Self]]:
        """Возвращает промпты категории"""

        query = sa.select(cls).where(cls.category_id == category_id, cls.is_active == True).order_by(cls.ordering)

        async with begin_connection() as conn:
            result = await conn.execute(query)

        return result.scalars().all()

    @classmethod
    async def get_prompt_with_category(cls, prompt_id: int) -> t.Optional[t.Self]:
        """Возвращает промпты категории"""

        query = (
            sa.select(cls).options(joinedload(cls.prompt_category))
            .where(cls.id == prompt_id)
        )

        # query = sa.select(cls).where(cls.category_id == category_id, cls.is_active == True)

        async with begin_connection() as conn:
            result = await conn.execute(query)

        return result.scalars().first()
