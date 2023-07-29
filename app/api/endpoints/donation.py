from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User, CharityProject
from app.schemas.donation import DonationUserDB, DonationCreate, DonationSuperuserDB
from app.services.investment import investment

router = APIRouter()


@router.post(
    '/',
    response_model=DonationUserDB,
    response_model_exclude_none=True,
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),

) -> DonationUserDB:
    """
    Только для зарегистрированных пользователей.
    Создаёт пожервтование.
    """
    new_donation = await donation_crud.create(
        donation,
        session,
        user
    )
    await investment(
        new_donation,
        CharityProject,  # noqa
        session
    )
    return new_donation


@router.get(
    '/',
    response_model=List[DonationSuperuserDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donation(
        session: AsyncSession = Depends(get_async_session)
) -> List[DonationSuperuserDB]:
    """
    Только для суперюзеров.
    Возвращает все сделанные донаты.
    """
    donations = await donation_crud.get_multi(
        session
    )
    return donations


@router.get(
    '/my',
    response_model=List[DonationUserDB]
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> List[DonationUserDB]:
    """
    Только для зарегистрированных пользователей.
    Возвращает донаты конкретного пользователя.
    """
    donation = await donation_crud.get_by_user(
        user,
        session
    )
    return donation
