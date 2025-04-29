import axios from 'axios';
import googleSheetsConfig from '../config/googleSheets.config';

/**
 * Создает заголовки с токеном авторизации для запроса к Google API
 * @returns {Object} Заголовки запроса с токеном
 */
async function getAuthHeaders() {
  try {
    // Отправляем запрос на сервер для получения токена
    // В реальном приложении это должно быть реализовано на бэкенде для безопасности
    const response = await axios.post('/api/google-sheets/auth', {
      credentials: googleSheetsConfig.credentials
    });

    return {
      'Authorization': `Bearer ${response.data.token}`,
      'Content-Type': 'application/json'
    };
  } catch (error) {
    console.error('Ошибка при получении токена авторизации:', error);
    // Возвращаем заголовки без токена - запрос, вероятно, не пройдет,
    // но хотя бы не будет ошибки при выполнении кода
    return {
      'Content-Type': 'application/json'
    };
  }
}

/**
 * Получает список листов таблицы
 * @param {string} spreadsheetId ID Google таблицы (если не указан, берется из конфига)
 * @returns {Promise<Object>} Объект с листами таблицы
 */
export async function getWorksheets(spreadsheetId = googleSheetsConfig.spreadsheetId) {
  try {
    // Пытаемся получить данные напрямую через API бэкенда
    const response = await axios.get(
      `/api/google-sheets/spreadsheets/${spreadsheetId}/worksheets`,
      {
        params: {
          serviceAccount: googleSheetsConfig.botName
        }
      }
    );
    return response.data;
  } catch (error) {
    console.error('Ошибка при получении списка листов:', error);
    throw error;
  }
}

/**
 * Получает данные из указанного диапазона листа
 * @param {string} spreadsheetId ID Google таблицы (если не указан, берется из конфига)
 * @param {string} range Диапазон данных (например, "Sheet1!A1:Z100")
 * @returns {Promise<Array>} Массив данных из таблицы
 */
export async function getSheetData(
  spreadsheetId = googleSheetsConfig.spreadsheetId,
  range = googleSheetsConfig.displaySettings.dataRange
) {
  try {
    // Если не указан лист в диапазоне, используем лист по умолчанию
    if (!range.includes('!')) {
      range = `${googleSheetsConfig.defaultSheetId}!${range}`;
    }

    const response = await axios.get(
      `/api/google-sheets/spreadsheets/${spreadsheetId}/values/${range}`,
      {
        params: {
          serviceAccount: googleSheetsConfig.botName
        }
      }
    );
    return response.data;
  } catch (error) {
    console.error('Ошибка при получении данных листа:', error);
    throw error;
  }
}

/**
 * Обновляет данные в указанном диапазоне листа
 * @param {string} spreadsheetId ID Google таблицы (если не указан, берется из конфига)
 * @param {string} range Диапазон данных (например, "Sheet1!A1:Z100")
 * @param {Array} values Массив данных для обновления
 * @returns {Promise<Object>} Результат обновления
 */
export async function updateSheetData(
  spreadsheetId = googleSheetsConfig.spreadsheetId,
  range,
  values
) {
  try {
    // Если не указан лист в диапазоне, используем лист по умолчанию
    if (!range.includes('!')) {
      range = `${googleSheetsConfig.defaultSheetId}!${range}`;
    }

    const response = await axios.put(
      `/api/google-sheets/spreadsheets/${spreadsheetId}/values/${range}`,
      {
        values,
        serviceAccount: googleSheetsConfig.botName
      }
    );
    return response.data;
  } catch (error) {
    console.error('Ошибка при обновлении данных листа:', error);
    throw error;
  }
}

/**
 * Создает новый лист в таблице
 * @param {string} spreadsheetId ID Google таблицы (если не указан, берется из конфига)
 * @param {string} title Название нового листа
 * @returns {Promise<Object>} Созданный лист
 */
export async function createWorksheet(
  spreadsheetId = googleSheetsConfig.spreadsheetId,
  title
) {
  try {
    const response = await axios.post(
      `/api/google-sheets/spreadsheets/${spreadsheetId}/worksheets`,
      {
        title,
        serviceAccount: googleSheetsConfig.botName
      }
    );
    return response.data;
  } catch (error) {
    console.error('Ошибка при создании нового листа:', error);
    throw error;
  }
}

// Генерирует тестовые данные листов для отладки
function getMockWorksheets() {
  return {
    worksheets: [
      { id: 1, title: "Лист1", index: 0, rowCount: 100, columnCount: 26 },
      { id: 2, title: "Лист2", index: 1, rowCount: 50, columnCount: 15 },
      { id: 3, title: "Данные", index: 2, rowCount: 200, columnCount: 10 }
    ]
  };
}

// Генерирует тестовые данные листа для отладки
function getMockSheetData(worksheet) {
  if (worksheet === "Лист1" || (worksheet && worksheet.title === "Лист1")) {
    return [
      ["Имя", "Фамилия", "Возраст", "Город"],
      ["Иван", "Иванов", "25", "Москва"],
      ["Петр", "Петров", "30", "Санкт-Петербург"],
      ["Мария", "Сидорова", "28", "Казань"]
    ];
  } else if (worksheet === "Данные" || (worksheet && worksheet.title === "Данные")) {
    return [
      ["Дата", "Показатель 1", "Показатель 2", "Показатель 3"],
      ["01.01.2025", "120", "45", "67"],
      ["02.01.2025", "135", "48", "71"],
      ["03.01.2025", "142", "52", "75"],
      ["04.01.2025", "128", "43", "69"]
    ];
  } else {
    return [
      ["Заголовок 1", "Заголовок 2", "Заголовок 3"],
      ["Значение 1", "Значение 2", "Значение 3"],
      ["Значение 4", "Значение 5", "Значение 6"]
    ];
  }
}

// Экспорт функций как именованных и как объекта по умолчанию
export default {
  getWorksheets,
  getSheetData,
  updateSheetData,
  createWorksheet,

  // Мок-функции для отладки интерфейса
  getMockWorksheets,
  getMockSheetData,

  // Информация из конфига для удобства
  config: {
    spreadsheetId: googleSheetsConfig.spreadsheetId,
    defaultSheetId: googleSheetsConfig.defaultSheetId,
    autoRefreshInterval: googleSheetsConfig.displaySettings.autoRefreshInterval || 60000
  }
};
