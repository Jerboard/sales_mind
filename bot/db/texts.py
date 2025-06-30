import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, begin_connection


class Text(Base):
    __tablename__ = "texts"

    key: Mapped[str] = mapped_column(sa.String(255))
    text: Mapped[str] = mapped_column(sa.Text)

    def __repr__(self): return f"<Text id={self.id} key={self.key}>"

    _cache = {}

    @classmethod
    async def get_text(cls, key: int) -> str:
        """Возвращает текст"""
        # if key in cls._cache:
        #     return cls._cache[key]

        query = sa.select(cls).where(cls.key == key)

        async with begin_connection() as conn:
            result = await conn.execute(query)
            text = result.scalars().first().text
            cls._cache[key] = text

        return text if text else f'‼️ Нет текста  ключ: {key}'
