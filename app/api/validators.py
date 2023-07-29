from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession
) -> None:
    """Проверка наличия дублирующихся имён."""
    charity_id = await charity_project_crud.get_charity_project_by_id(
        charity_project_name,
        session
    )
    if charity_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """
    Проверяет, существует ли проект с указанным ID.
    """
    charity_project = await charity_project_crud.get(
        charity_project_id,
        session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Не найден проект!'
        )
    return charity_project


async def check_project_close(
        project: CharityProject
) -> None:
    """Проверка проекта на состояние: закрыт."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Удаление закрытых проектов - запрещено!'
        )


async def check_charity_project_close(
    project: CharityProject,
) -> None:
    """Проверяет, закрыт проект или нет."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_invested_before_edit(
    project: CharityProject,
    project_request: CharityProjectUpdate,
) -> None:
    """Проверяет сумму, инвестированную в проект при обновлении проекта."""
    if (project_request.full_amount is not None and
            project.invested_amount > project_request.full_amount):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя установить сумму, ниже уже вложенной!'
        )


async def check_invested_before_delete(
    project: CharityProject,
) -> None:
    """Проверяет сумму, инвестированную в проект при удалении проекта."""
    if project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
