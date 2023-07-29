from typing import Optional, Union, Dict, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User
from app.models.donation import Donation


class CRUDDonation(CRUDBase):
    @staticmethod
    async def get_by_user(
            user: User,
            session: AsyncSession
    ) -> List[Donation]:
        donation_all = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donation_all.scalars().all()

    async def create(
            self,
            obj_in: Union[Donation, Dict],
            session: AsyncSession,
            user: Optional[User] = None
    ) -> Union[Donation]:
        """Переписывает базовый метод."""
        obj_in_data = obj_in.dict()
        obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


donation_crud = CRUDDonation(Donation)
