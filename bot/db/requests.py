from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date, time
from sqlalchemy.dialects import postgresql as psql

import sqlalchemy as sa
import typing as t

from .base import Base, begin_connection


class Request(Base):
    __tablename__ = "requests"

    price: Mapped[float] = mapped_column(sa.Numeric(10, 2))
    response_count: Mapped[int] = mapped_column(sa.Integer, default=0)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)

    ordering: Mapped[int] = mapped_column(sa.Integer, default=1)

