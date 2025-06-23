import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from .base import Base

class Tariff(Base):
    __tablename__ = "tariffs"

    name: Mapped[str] = mapped_column(sa.String(100))
    description: Mapped[str] = mapped_column(sa.Text)
    price: Mapped[float] = mapped_column(sa.Numeric(10, 2))
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)

    def __repr__(self) -> str:
        return f"<Tariff id={self.id} name='{self.name}'>"