from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession


from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    @staticmethod
    async def get_charity_project_by_id(
            charity_project_name: str,
            session: AsyncSession,
    ) -> Optional[CharityProject]:
        """Метод получения ID проекта по его имени."""
        charity_project = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        return charity_project.scalars().first()

    @staticmethod
    async def get_projects_by_completion_rate(
            session: AsyncSession,
    ) -> List[CharityProject]:
        """Метод получения списка проектов которые 'закрыты'. """
        close_charity_project = await session.execute(
            select([CharityProject.name,
                    (
                            func.julianday(CharityProject.close_date) -
                            func.julianday(CharityProject.create_date)
                     ).label('life_duration'),
                    CharityProject.description
                    ]).where(
                CharityProject.fully_invested
            ).order_by('life_duration')
        )
        return close_charity_project.all() or []


charity_project_crud = CRUDCharityProject(CharityProject)
