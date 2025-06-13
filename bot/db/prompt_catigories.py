from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date, time
from sqlalchemy.dialects import postgresql as psql

import sqlalchemy as sa
import typing as t

from .base import Base, begin_connection


class PromptCategory(Base):
    __tablename__ = "prompt_categories"

    name: Mapped[str] = mapped_column(sa.String(255))
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
