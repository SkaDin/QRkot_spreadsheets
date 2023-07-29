from sqlalchemy import Column, Text, String

from app.models.base import AbstractBase


class CharityProject(AbstractBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
