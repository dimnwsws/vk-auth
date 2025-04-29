from fastapi import APIRouter, HTTPException, Depends, Body, Query
from typing import List, Optional, Dict, Any
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

router = APIRouter(
    prefix="/google-sheets",
    tags=["google-sheets"],
)


# Функция для создания сервиса Google Sheets
def get_sheets_service(service_account_info):
    """
    Создает и возвращает сервис Google Sheets API
    """
    try:
        # Указываем необходимые права доступа
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        # Создаем учетные данные из информации о сервисном аккаунте
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES
        )

        # Создаем сервис Google Sheets API
        service = build('sheets', 'v4', credentials=credentials)

        return service
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при инициализации Google Sheets API: {str(e)}"
        )


# Эндпоинт для получения токена авторизации
@router.post("/auth")
async def get_auth_token(credentials: dict = Body(...)):
    """
    Получает токен авторизации для Google API
    """
    try:
        # Здесь должна быть логика получения токена
        # Обычно это не нужно реализовывать на фронтенде,
        # так как учетные данные сервисного аккаунта должны храниться на сервере

        # Для демонстрации возвращаем заглушку
        return {"token": "dummy_token_for_demo"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении токена: {str(e)}"
        )


# Эндпоинт для получения списка листов
@router.get("/spreadsheets/{spreadsheet_id}/worksheets")
async def get_worksheets(
        spreadsheet_id: str,
        service_account: Optional[str] = Query(None),
        credentials: Optional[Dict[str, Any]] = Body(None)
):
    """
    Получает список листов из таблицы Google Sheets
    """
    try:
        # Здесь должна быть логика получения учетных данных сервисного аккаунта
        # В реальном приложении они должны храниться в безопасном месте на сервере

        # Для демонстрации используем переданные учетные данные
        # или загружаем их из конфигурационного файла
        service_account_info = credentials

        # Получаем сервис Google Sheets API
        service = get_sheets_service(service_account_info)

        # Получаем информацию о таблице
        spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

        # Извлекаем информацию о листах
        worksheets = []
        for sheet in spreadsheet.get('sheets', []):
            properties = sheet.get('properties', {})
            grid_properties = properties.get('gridProperties', {})

            worksheets.append({
                'id': properties.get('sheetId'),
                'title': properties.get('title'),
                'index': properties.get('index'),
                'rowCount': grid_properties.get('rowCount'),
                'columnCount': grid_properties.get('columnCount')
            })

        return {"worksheets": worksheets}
    except HttpError as error:
        if error.resp.status == 404:
            raise HTTPException(
                status_code=404,
                detail=f"Таблица не найдена: {spreadsheet_id}"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка Google API: {str(error)}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении листов: {str(e)}"
        )


# Эндпоинт для получения данных из листа
@router.get("/spreadsheets/{spreadsheet_id}/values/{range}")
async def get_values(
        spreadsheet_id: str,
        range: str,
        service_account: Optional[str] = Query(None),
        credentials: Optional[Dict[str, Any]] = Body(None)
):
    """
    Получает данные из указанного диапазона листа Google Sheets
    """
    try:
        # Получаем учетные данные сервисного аккаунта
        service_account_info = credentials

        # Получаем сервис Google Sheets API
        service = get_sheets_service(service_account_info)

        # Получаем данные из указанного диапазона
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range
        ).execute()

        values = result.get('values', [])

        return values
    except HttpError as error:
        if error.resp.status == 404:
            raise HTTPException(
                status_code=404,
                detail=f"Таблица или диапазон не найдены"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка Google API: {str(error)}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении данных: {str(e)}"
        )


# Эндпоинт для обновления данных в листе
@router.put("/spreadsheets/{spreadsheet_id}/values/{range}")
async def update_values(
        spreadsheet_id: str,
        range: str,
        values: List[List[Any]] = Body(..., embed=True),
        service_account: Optional[str] = Query(None),
        credentials: Optional[Dict[str, Any]] = Body(None)
):
    """
    Обновляет данные в указанном диапазоне листа Google Sheets
    """
    try:
        # Получаем учетные данные сервисного аккаунта
        service_account_info = credentials

        # Получаем сервис Google Sheets API
        service = get_sheets_service(service_account_info)

        # Подготавливаем тело запроса
        body = {
            'values': values
        }

        # Обновляем данные
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()

        return result
    except HttpError as error:
        if error.resp.status == 404:
            raise HTTPException(
                status_code=404,
                detail=f"Таблица или диапазон не найдены"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка Google API: {str(error)}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при обновлении данных: {str(e)}"
        )


# Эндпоинт для создания нового листа
@router.post("/spreadsheets/{spreadsheet_id}/worksheets")
async def create_worksheet(
        spreadsheet_id: str,
        title: str = Body(..., embed=True),
        service_account: Optional[str] = Query(None),
        credentials: Optional[Dict[str, Any]] = Body(None)
):
    """
    Создает новый лист в таблице Google Sheets
    """
    try:
        # Получаем учетные данные сервисного аккаунта
        service_account_info = credentials

        # Получаем сервис Google Sheets API
        service = get_sheets_service(service_account_info)

        # Подготавливаем запрос на создание нового листа
        request = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": title
                        }
                    }
                }
            ]
        }

        # Выполняем запрос
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=request
        ).execute()

        # Получаем информацию о созданном листе
        new_sheet = response.get('replies', [])[0].get('addSheet', {}).get('properties', {})

        return {
            'id': new_sheet.get('sheetId'),
            'title': new_sheet.get('title'),
            'index': new_sheet.get('index'),
            'rowCount': new_sheet.get('gridProperties', {}).get('rowCount'),
            'columnCount': new_sheet.get('gridProperties', {}).get('columnCount')
        }
    except HttpError as error:
        if error.resp.status == 404:
            raise HTTPException(
                status_code=404,
                detail=f"Таблица не найдена: {spreadsheet_id}"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка Google API: {str(error)}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при создании листа: {str(e)}"
        )