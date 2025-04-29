<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-4">Интеграция с Google Sheets</h2>

    <div class="mb-6">
      <div class="flex items-center mb-4">
        <input
          v-model="spreadsheetId"
          type="text"
          placeholder="ID Google Таблицы"
          class="flex-grow bg-gray-700 text-white px-4 py-2 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          @click="fetchWorksheets"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-r-md transition-colors"
        >
          Загрузить
        </button>
      </div>
      <p class="text-sm text-gray-400">
        ID таблицы можно найти в URL: https://docs.google.com/spreadsheets/d/<span class="text-yellow-400">ID_ТАБЛИЦЫ</span>/edit
      </p>
    </div>

    <!-- Индикатор загрузки -->
    <div v-if="loading" class="flex justify-center py-6">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>

    <!-- Сообщение об ошибке -->
    <div v-if="error" class="bg-red-900/30 p-4 rounded-lg text-red-200 mb-6">
      {{ error }}
    </div>

    <!-- Список листов -->
    <div v-if="worksheets.length > 0" class="mb-8">
      <h3 class="text-xl font-semibold mb-4">Доступные листы</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="worksheet in worksheets"
          :key="worksheet.id"
          :class="[
            'bg-gray-700 rounded-lg p-4 cursor-pointer transition-colors',
            selectedWorksheet && selectedWorksheet.id === worksheet.id
              ? 'border-2 border-blue-500'
              : 'hover:bg-gray-600'
          ]"
          @click="selectWorksheet(worksheet)"
        >
          <h4 class="font-medium text-lg mb-1">{{ worksheet.title }}</h4>
          <p class="text-gray-400 text-sm">
            {{ worksheet.rowCount || '?' }} строк × {{ worksheet.columnCount || '?' }} столбцов
          </p>
        </div>
      </div>
    </div>

    <!-- Содержимое выбранного листа -->
    <div v-if="selectedWorksheet && !dataLoading && !dataError" class="mb-8">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-xl font-semibold">{{ selectedWorksheet.title }}</h3>
        <div class="flex space-x-2">
          <button
            @click="refreshSheetData"
            class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded-md text-sm transition-colors flex items-center"
          >
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
            Обновить
          </button>
          <button
            @click="exportToCsv"
            class="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded-md text-sm transition-colors flex items-center"
          >
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
            </svg>
            Экспорт
          </button>
        </div>
      </div>

      <!-- Таблица с данными -->
      <div class="overflow-x-auto">
        <table class="min-w-full bg-gray-700 rounded-lg overflow-hidden">
          <thead class="bg-gray-600">
            <tr>
              <th
                v-for="(cell, index) in sheetData[0] || []"
                :key="index"
                class="py-3 px-4 text-left text-xs font-medium text-gray-300 uppercase tracking-wider"
              >
                {{ cell }}
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-600">
            <tr v-for="(row, rowIndex) in sheetData.slice(1)" :key="rowIndex" class="hover:bg-gray-600">
              <td
                v-for="(cell, cellIndex) in row"
                :key="cellIndex"
                class="py-2 px-4 text-sm text-gray-300"
              >
                {{ cell }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Индикатор загрузки данных листа -->
    <div v-else-if="dataLoading" class="flex justify-center py-6">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>

    <!-- Сообщение об ошибке при загрузке данных листа -->
    <div v-else-if="dataError" class="bg-red-900/30 p-4 rounded-lg text-red-200 mb-6">
      {{ dataError }}
    </div>
  </div>
</template>

<script>
import googleSheetsAPI from '../services/googleSheetsAPI';

export default {
  name: 'GoogleSheetsIntegration',
  data() {
    return {
      spreadsheetId: '1QWoH_teqJTcymYwa7H3kljWKyPS5NTLcVSUb9J6otaw', // Значение по умолчанию
      worksheets: [],
      selectedWorksheet: null,
      sheetData: [],
      loading: false,
      error: null,
      dataLoading: false,
      dataError: null
    };
  },
  mounted() {
    // Автоматически загружаем листы при монтировании компонента
    this.fetchWorksheets();
  },
  methods: {
    async fetchWorksheets() {
      if (!this.spreadsheetId) {
        this.error = 'Введите ID Google таблицы';
        return;
      }

      this.loading = true;
      this.error = null;
      this.worksheets = [];

      try {
        // Пытаемся получить данные от API
        try {
          const data = await googleSheetsAPI.getWorksheets(this.spreadsheetId);
          this.worksheets = data.worksheets || [];
        } catch (e) {
          console.warn('Используем тестовые данные вместо API:', e);
          // Используем мок-данные, если API недоступен
          const mockData = googleSheetsAPI.getMockWorksheets();
          this.worksheets = mockData.worksheets;
        }

        // Если есть доступные листы, выбираем первый по умолчанию
        if (this.worksheets.length > 0 && !this.selectedWorksheet) {
          this.selectWorksheet(this.worksheets[0]);
        }
      } catch (error) {
        console.error('Ошибка при загрузке листов:', error);
        this.error = `Ошибка при загрузке листов: ${error.message || 'Неизвестная ошибка'}`;
      } finally {
        this.loading = false;
      }
    },

    selectWorksheet(worksheet) {
      this.selectedWorksheet = worksheet;
      this.refreshSheetData();
    },

    async refreshSheetData() {
      if (!this.selectedWorksheet) return;

      this.dataLoading = true;
      this.dataError = null;

      try {
        // Пытаемся загрузить данные через API
        try {
          const range = `${this.selectedWorksheet.title}!A1:Z1000`;
          const data = await googleSheetsAPI.getSheetData(this.spreadsheetId, range);
          this.sheetData = data || [];
        } catch (e) {
          console.warn('Используем тестовые данные для листа:', e);
          // Используем мок-данные, если API недоступен
          this.sheetData = googleSheetsAPI.getMockSheetData(this.selectedWorksheet);
        }
      } catch (error) {
        console.error('Ошибка при загрузке данных листа:', error);
        this.dataError = `Ошибка при загрузке данных: ${error.message || 'Неизвестная ошибка'}`;
      } finally {
        this.dataLoading = false;
      }
    },

    exportToCsv() {
      if (!this.sheetData || this.sheetData.length === 0) {
        return;
      }

      try {
        // Преобразуем данные в формат CSV
        const csvContent = this.sheetData
          .map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
          .join('\n');

        // Создаем Blob и ссылку для скачивания
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.setAttribute('href', url);
        link.setAttribute('download', `${this.selectedWorksheet.title}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } catch (error) {
        console.error('Ошибка при экспорте в CSV:', error);
        alert(`Ошибка при экспорте: ${error.message || 'Неизвестная ошибка'}`);
      }
    }
  }
};
</script>
