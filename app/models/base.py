from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class AbstractBase(Base):
    """Базовый абстрактный класс."""

    __abstract__ = True
    full_amount = Column(Integer, default=0)  # поле требуемой суммы
    invested_amount = Column(Integer, default=0)  # поле внесённой суммы
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime)
