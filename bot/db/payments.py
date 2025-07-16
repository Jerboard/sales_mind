from sqlalchemy.orm import Mapped, mapped_column

import sqlalchemy as sa
import typing as t

from .base import Base, begin_connection


class Payment(Base):
    __tablename__ = "payments"

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
    tariff_id: Mapped[int] = mapped_column(sa.ForeignKey("tariffs.id"), nullable=True)

    amount: Mapped[float] = mapped_column(sa.Float)
    payment_id: Mapped[str] = mapped_column(sa.String)

    # user: Mapped["User"] = relationship(back_populates="payments")
    # tariff: Mapped["Tariff"] = relationship(back_populates="payments")

    @classmethod
    async def add(
            cls,
            user_id: int,
            amount: float,
            payment_id: str,
            tariff_id: int = None,
    ) -> int:
        """
        Создаёт и сохраняет запись Payment.
        Возвращает уже обновлённый объект.
        """
        query = sa.insert(cls).values(
            user_id=user_id,
            tariff_id=tariff_id,
            amount=amount,
            payment_id=payment_id,
        )

        async with begin_connection() as conn:
            result = await conn.execute(query)
            await conn.commit()
        return result.inserted_primary_key[0]

    @classmethod
    async def get_last_for_user(cls, user_id: int) -> t.Optional[t.Self]:
        query = (
            sa.select(cls)
            .where(cls.user_id == user_id)
            .order_by(sa.desc(cls.created_at))
            .limit(1)
        )

        async with begin_connection() as conn:
            result = await conn.execute(query)

        return result.scalars().first()
