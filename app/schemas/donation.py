from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    """Базовая схема."""
    comment: Optional[str]
    full_amount: PositiveInt


class DonationCreate(DonationBase):
    """Схема создания пожертвований."""
    pass


class DonationUserDB(DonationCreate):
    """Схема для вывода информации обычным пользователям"""
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationSuperuserDB(DonationUserDB):
    """Схема для вывода информации суперюзерам."""
    user_id: int
    invested_amount: int = 0
    fully_invested: bool = False
    close_date: datetime = None

    class Config:
        orm_mode = True
