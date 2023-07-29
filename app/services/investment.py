from datetime import datetime
from typing import Union, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import TWO_MODEL_UNION
from app.models import CharityProject, Donation


async def close(
        obj: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:
    """Закрывает объект и добавляет дату закрытия."""
    if obj.full_amount == obj.invested_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now()
    return obj


async def reinvestment(
        new_obj: TWO_MODEL_UNION,
        open_obj: TWO_MODEL_UNION,
) -> Tuple[TWO_MODEL_UNION, TWO_MODEL_UNION]:
    """Перераспределяет средства между проектами и пожертвованиями."""
    # Вычисляем оставшуюся сумму, которую нужно вложить в новый проект.
    to_close_new_obj = new_obj.full_amount - new_obj.invested_amount
    # Вычисляем оставшуюся сумму,
    # которую нужно вложить в открытый проект.
    to_close_open_obj = open_obj.full_amount - open_obj.invested_amount
    # Если "to_close_new_obj" меньше или равна, то это означает,
    # что в новый проект можно вложить все оставшиеся средства.
    if to_close_new_obj <= to_close_open_obj:
        open_obj.invested_amount += to_close_new_obj
        new_obj.invested_amount += to_close_new_obj
    # Иначе "to_close_new_obj" больше "to_close_open_obj",
    # то это означает, что оставшихся средств недостаточно
    # для полного вложения в новый проект.
    else:
        open_obj.invested_amount += to_close_open_obj
        to_close_new_obj -= to_close_open_obj
        new_obj.invested_amount += to_close_open_obj
    return new_obj, open_obj


async def investment(
        new_obj: TWO_MODEL_UNION,
        model: TWO_MODEL_UNION,
        session: AsyncSession,
) -> None:
    """Инвестирование или переинвестирование объекта `new_obj`."""
    all_open_obj = await session.execute(
        select(model).where(model.fully_invested == False)  # noqa
    )
    all_open_obj = all_open_obj.scalars().all()
    for open_obj in all_open_obj:
        new_obj, open_obj = await reinvestment(new_obj, open_obj)
        if open_obj.invested_amount == open_obj.full_amount:
            open_obj = await close(open_obj)
        session.add(open_obj)
        if new_obj.invested_amount == new_obj.full_amount:
            new_obj = await close(new_obj)
            break
    session.add(new_obj)
    await session.commit()
    await session.refresh(new_obj)
