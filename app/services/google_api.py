from datetime import datetime, timedelta
from typing import List

from aiogoogle import Aiogoogle

from app.core.config import settings


FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(
        wrapper_services: Aiogoogle
) -> str:
    now_date_time = datetime.now().strftime(FORMAT)

    service = await wrapper_services.discover('sheets', 'v4')

    spreadsheet_body = {
        'properties': {
            'title': f'Отчёт на {now_date_time}',
            'locale': 'ru_RU',
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Лист1',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 11
                }
            }
        }]
    }

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )

    spreadsheet_id = response['spreadsheetId']

    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_service: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_service.discover('drive', 'v3')

    await wrapper_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: List,
        wrapper_service: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)

    service = await wrapper_service.discover('sheets', 'v4')

    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    for result in charity_projects:
        new_row = [
            result.name,
            str(timedelta(days=result[1])),
            result.description
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    response = await wrapper_service.as_service_account( # noqa
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
