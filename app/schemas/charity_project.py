from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator, Extra


class CharityProjectBase(BaseModel):
    """Базовая схема."""
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )
    description: str = Field(
        ...,
        min_length=1,
    )
    full_amount: PositiveInt

    @validator('name')
    def validate_name(cls, value): # noqa
        """Проверка имени на пустоту."""
        if not value:
            raise ValueError('Имя не может быть пустым!')
        return value

class CharityProjectCreate(CharityProjectBase):
    """Схема создания благотварительных проектов."""
    pass


class CharityProjectUpdate(CharityProjectBase):
    """Схема редактирования проектов."""
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100
    )
    description: Optional[str] = Field(
        None,
        min_length=1
    )
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    """Схема вывода данных из БД."""
    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: datetime = None

    class Config:
        orm_mode = True
