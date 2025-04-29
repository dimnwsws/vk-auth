import os
import json
from typing import Dict, List, Any, Optional
import gspread
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials


class GoogleSheetsService:
    """Сервис для работы с Google Sheets API"""

    def __init__(self):
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

    def _get_credentials(self, credentials_dict: Dict) -> Credentials:
        """Получение учетных данных из словаря"""
        return service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=self.scopes
        )

    def get_client(self, credentials: Dict) -> gspread.Client:
        """Получение клиента gspread"""
        creds = self._get_credentials(credentials)
        return gspread.authorize(creds)

    def get_worksheets(self, spreadsheet_id: str, credentials: Dict) -> List[Dict]:
        """Получение списка листов в таблице"""
        client = self.get_client(credentials)
        spreadsheet = client.open_by_key(spreadsheet_id)

        worksheets = []
        for worksheet in spreadsheet.worksheets():
            worksheets.append({
                'id': worksheet.id,
                'title': worksheet.title,
                'properties': {
                    'gridProperties': {
                        'rowCount': worksheet.row_count,
                        'columnCount': worksheet.col_count
                    }
                }
            })

        return worksheets

    def get_worksheet_data(self, spreadsheet_id: str, worksheet_id: str, config: Dict, credentials: Dict) -> List[
        List[Any]]:
        """Получение данных из листа"""
        client = self.get_client(credentials)
        spreadsheet = client.open_by_key(spreadsheet_id)

        # Попытка найти лист по ID или названию
        worksheet = None
        try:
            # Пробуем найти по ID
            worksheet = spreadsheet.get_worksheet_by_id(int(worksheet_id))
        except (ValueError, gspread.exceptions.WorksheetNotFound):
            # Пробуем найти по названию
            for sheet in spreadsheet.worksheets():
                if sheet.title.lower() == worksheet_id.lower():
                    worksheet = sheet
                    break

        if not worksheet:
            raise ValueError(f"Лист с ID или названием '{worksheet_id}' не найден")

        # Получаем диапазон данных
        range_str = config.get('range', 'A1:Z1000')
        data = worksheet.get_values(range_str)

        return data

    def update_worksheet_data(self, spreadsheet_id: str, worksheet_id: str, update_data: Dict,
                              credentials: Dict) -> Dict:
        """Обновление данных в листе"""
        client = self.get_client(credentials)
        spreadsheet = client.open_by_key(spreadsheet_id)

        # Попытка найти лист по ID или названию
        worksheet = None
        try:
            # Пробуем найти по ID
            worksheet = spreadsheet.get_worksheet_by_id(int(worksheet_id))
        except (ValueError, gspread.exceptions.WorksheetNotFound):
            # Пробуем найти по названию
            for sheet in spreadsheet.worksheets():
                if sheet.title.lower() == worksheet_id.lower():
                    worksheet = sheet
                    break

        if not worksheet:
            raise ValueError(f"Лист с ID или названием '{worksheet_id}' не найден")

        range_str = update_data.get('range')
        values = update_data.get('values', [])

        if not range_str:
            raise ValueError("Не указан диапазон для обновления")

        worksheet.update(range_str, values)

        return {"updated": True, "updatedRange": range_str}

    def create_worksheet(self, spreadsheet_id: str, worksheet_data: Dict, credentials: Dict) -> Dict:
        """Создание нового листа в таблице"""
        client = self.get_client(credentials)
        spreadsheet = client.open_by_key(spreadsheet_id)

        title = worksheet_data.get('title')
        rows = worksheet_data.get('rows', 100)
        cols = worksheet_data.get('cols', 20)

        if not title:
            raise ValueError("Не указано название для нового листа")

        worksheet = spreadsheet.add_worksheet(title=title, rows=rows, cols=cols)

        return {
            'id': worksheet.id,
            'title': worksheet.title,
            'properties': {
                'gridProperties': {
                    'rowCount': worksheet.row_count,
                    'columnCount': worksheet.col_count
                }
            }
        }

    def delete_worksheet(self, spreadsheet_id: str, worksheet_id: str, credentials: Dict) -> Dict:
        """Удаление листа из таблицы"""
        client = self.get_client(credentials)
        spreadsheet = client.open_by_key(spreadsheet_id)

        # Попытка найти лист по ID или названию
        worksheet = None
        try:
            # Пробуем найти по ID
            worksheet = spreadsheet.get_worksheet_by_id(int(worksheet_id))
        except (ValueError, gspread.exceptions.WorksheetNotFound):
            # Пробуем найти по названию
            for sheet in spreadsheet.worksheets():
                if sheet.title.lower() == worksheet_id.lower():
                    worksheet = sheet
                    break

        if not worksheet:
            raise ValueError(f"Лист с ID или названием '{worksheet_id}' не найден")

        spreadsheet.del_worksheet(worksheet)

        return {"deleted": True, "worksheetId": worksheet_id}

    def append_rows(self, spreadsheet_id: str, worksheet_id: str, rows: List[List[Any]], credentials: Dict) -> Dict:
        """Добавление новых строк в лист"""
        client = self.get_client(credentials)
        spreadsheet = client.open_by_key(spreadsheet_id)

        # Попытка найти лист по ID или названию
        worksheet = None
        try:
            # Пробуем найти по ID
            worksheet = spreadsheet.get_worksheet_by_id(int(worksheet_id))
        except (ValueError, gspread.exceptions.WorksheetNotFound):
            # Пробуем найти по названию
            for sheet in spreadsheet.worksheets():
                if sheet.title.lower() == worksheet_id.lower():
                    worksheet = sheet
                    break

        if not worksheet:
            raise ValueError(f"Лист с ID или названием '{worksheet_id}' не найден")

        result = worksheet.append_rows(rows)

        return {"appended": True, "rowsCount": len(rows)}

    def get_spreadsheet_metadata(self, spreadsheet_id: str, credentials: Dict) -> Dict:
        """Получение метаданных о таблице"""
        client = self.get_client(credentials)
        spreadsheet = client.open_by_key(spreadsheet_id)

        return {
            'id': spreadsheet.id,
            'title': spreadsheet.title,
            'url': spreadsheet.url,
            'worksheetsCount': len(spreadsheet.worksheets())
        }