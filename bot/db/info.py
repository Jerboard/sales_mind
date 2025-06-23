import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from .base import Base


class Info(Base):
    __tablename__ = "info"

    name: Mapped[str] = mapped_column(sa.String(100))
    description: Mapped[str] = mapped_column(sa.Text)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)

    def __repr__(self) -> str: return f"<Info id={self.id} name='{self.name}'>"