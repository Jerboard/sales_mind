import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, begin_connection
from enums import HandlerKey


class Text(Base):
    __tablename__ = "texts"

    key: Mapped[str] = mapped_column(sa.String(255))
    text: Mapped[str] = mapped_column(sa.Text)
    ordering: Mapped[int] = mapped_column(sa.Integer, default=1)

    def __repr__(self): return f"<Text id={self.id} key={self.key}>"

    _cache = {}

    @classmethod
    async def add_new_texts_on_start(cls):
        async with begin_connection() as conn:
            for key in HandlerKey:
                if not key.with_text:
                    continue
                query = sa.select(cls).where(cls.key == key.key)
                result = await conn.execute(query)
                result = result.scalars().first()

                if not result:
                    query = sa.insert(cls).values(key=key.key, text=key.label)
                    await conn.execute(query)
                    await conn.commit()


    @classmethod
    async def get_text(cls, key: str) -> str:
        """Возвращает текст"""
        # if key in cls._cache:
        #     return cls._cache[key]

        query = sa.select(cls).where(cls.key == key)

        async with begin_connection() as conn:
            result = await conn.execute(query)
            result = result.scalars().first()

        if result:
            cls._cache[key] = result.text
            return result.text
        else:
            return f'‼️ Нет текста  ключ: {key}'
