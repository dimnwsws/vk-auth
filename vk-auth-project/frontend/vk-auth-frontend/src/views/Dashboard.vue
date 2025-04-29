<template>
  <div class="min-h-screen bg-gray-900 text-gray-200">
    <!-- Верхняя панель навигации -->
    <header class="bg-gray-800 shadow-md">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <h1 class="text-xl font-bold">Phantom Site</h1>

        <!-- Профиль пользователя -->
        <div class="relative group">
          <div class="flex items-center cursor-pointer">
            <img
              v-if="user && user.photo_url"
              :src="user.photo_url"
              alt="Фото профиля"
              class="w-10 h-10 rounded-full border-2 border-gray-700 transition-transform hover:scale-105"
            >
            <div
              v-else
              class="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center border-2 border-gray-700 transition-transform hover:scale-105"
            >
              <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </div>

            <!-- Выпадающее меню -->
            <div class="absolute right-0 top-12 w-56 bg-gray-800 rounded-lg shadow-xl py-2 z-50 hidden group-hover:block">
              <div class="px-4 py-2 border-b border-gray-700">
                <p class="font-medium">{{ user ? `${user.first_name} ${user.last_name}` : 'Загрузка...' }}</p>
                <p class="text-sm text-gray-400">{{ roleName }}</p>
              </div>
              <router-link to="/profile" class="block px-4 py-2 hover:bg-gray-700 transition-colors">
                Мой профиль
              </router-link>
              <button @click="logout" class="block w-full text-left px-4 py-2 hover:bg-gray-700 text-red-400 transition-colors">
                Выйти
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <div class="flex min-h-screen">
      <!-- Боковая панель с кнопками -->
      <div class="w-64 bg-gray-800 shadow-lg">
        <div class="p-4 space-y-2">
          <h2 class="text-xl font-bold text-white mb-4">Меню</h2>

          <!-- Кнопка главной панели -->
          <div
            @click="activeSection = 'dashboard'"
            :class="['p-3 rounded-lg cursor-pointer transition-colors',
              activeSection === 'dashboard' ? 'bg-blue-600 text-white' : 'hover:bg-gray-700 text-gray-300']"
          >
            <div class="flex items-center space-x-3">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"></path>
              </svg>
              <span>Главная</span>
            </div>
          </div>

          <!-- Кнопка Google Таблиц -->
          <div
            @click="openGoogleSheets"
            :class="['p-3 rounded-lg cursor-pointer transition-colors',
              activeSection === 'tables' ? 'bg-blue-600 text-white' : 'hover:bg-gray-700 text-gray-300']"
          >
            <div class="flex items-center space-x-3">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
              </svg>
              <span>Google Таблицы</span>
            </div>
          </div>

          <!-- Кнопка админ-панели (только для админов) -->
          <div
            v-if="hasAdminAccess"
            @click="navigateToAdmin"
            :class="['p-3 rounded-lg cursor-pointer transition-colors',
              activeSection === 'admin' ? 'bg-blue-600 text-white' : 'hover:bg-gray-700 text-gray-300']"
          >
            <div class="flex items-center space-x-3">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"></path>
              </svg>
              <span>Админ панель</span>
            </div>
          </div>

          <!-- Кнопка подтверждения пользователей (только для админов) -->
          <div
            v-if="hasAdminAccess"
            @click="activeSection = 'approvals'"
            :class="['p-3 rounded-lg cursor-pointer transition-colors',
              activeSection === 'approvals' ? 'bg-blue-600 text-white' : 'hover:bg-gray-700 text-gray-300']"
          >
            <div class="flex items-center space-x-3">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span>Подтверждение пользователей</span>
              <div v-if="pendingUsers.length > 0" class="bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center">
                {{ pendingUsers.length }}
              </div>
            </div>
          </div>

          <!-- Разделитель -->
          <div class="border-t border-gray-700 my-4"></div>

          <!-- Листы Google Таблицы - появляются только когда активна секция таблиц -->
          <div v-if="activeSection === 'tables'">
            <h3 class="text-sm uppercase text-gray-500 font-semibold mb-2 px-3">Листы таблицы</h3>

            <!-- Индикатор загрузки листов -->
            <div v-if="loadingWorksheets" class="flex justify-center py-4">
              <div class="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-blue-500"></div>
            </div>

            <!-- Ошибка загрузки -->
            <div v-else-if="worksheetsError" class="text-red-400 text-sm px-3 py-2">
              Ошибка загрузки листов
            </div>

            <!-- Список листов -->
            <div v-else class="space-y-1 max-h-64 overflow-y-auto pr-2">
              <div
                v-for="worksheet in worksheets"
                :key="worksheet.id"
                :class="['p-2 rounded cursor-pointer text-sm transition-colors mx-1',
                  selectedWorksheet && selectedWorksheet.id === worksheet.id
                    ? 'bg-blue-600/60 text-white'
                    : 'hover:bg-gray-700 text-gray-300']"
                @click="selectWorksheet(worksheet)"
              >
                <div class="flex items-center space-x-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                  <span class="truncate">{{ worksheet.title }}</span>
                </div>
              </div>
            </div>

            <!-- Кнопка обновления листов -->
            <div class="mt-4 px-3">
              <button
                @click="refreshWorksheets"
                class="w-full bg-gray-700 hover:bg-gray-600 text-gray-300 py-2 px-3 rounded-md text-sm transition-colors flex items-center justify-center"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
                Обновить листы
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Основной контент -->
      <main class="flex-1 p-8">
        <!-- Приветствие на главной -->
        <div v-if="activeSection === 'dashboard'">
          <div class="mb-8">
            <h2 class="text-2xl font-bold mb-4">Добро пожаловать, {{ user ? user.first_name : 'Пользователь' }}!</h2>
            <p class="text-gray-400">Ваш статус: <span class="text-blue-400 font-medium">{{ roleName }}</span></p>
          </div>

          <!-- Карточки быстрого доступа -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- Карточка профиля -->
            <div class="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
              <div class="p-6">
                <h3 class="text-xl font-bold mb-2">Мой профиль</h3>
                <p class="text-gray-400 mb-4">Просмотр и управление личными данными</p>
                <router-link to="/profile" class="inline-block bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition-colors">
                  Перейти
                </router-link>
              </div>
            </div>

            <!-- Карточка Google таблиц -->
            <div class="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
              <div class="p-6">
                <h3 class="text-xl font-bold mb-2">Google Таблицы</h3>
                <p class="text-gray-400 mb-4">Просмотр и работа с Google таблицами</p>
                <button @click="openGoogleSheets" class="inline-block bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition-colors">
                  Открыть
                </button>
              </div>
            </div>

            <!-- Карточка администрирования (только для админов) -->
            <div v-if="hasAdminAccess" class="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
              <div class="p-6">
                <h3 class="text-xl font-bold mb-2">Администрирование сайта</h3>
                <p class="text-gray-400 mb-4">Управление пользователями и настройками</p>
                <router-link to="/admin" class="inline-block bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition-colors">
                  Перейти
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Контент Google Таблиц -->
        <div v-if="activeSection === 'tables'">
          <div class="mb-6">
            <h2 class="text-2xl font-bold mb-4">{{ selectedWorksheet ? selectedWorksheet.title : 'Google Таблицы' }}</h2>

            <!-- Информация о выбранном листе -->
            <div v-if="selectedWorksheet" class="text-gray-400 mb-6">
              <p>
                Лист: <span class="text-blue-400">{{ selectedWorksheet.title }}</span> &bull;
                {{ selectedWorksheet.rowCount || '?' }} строк &bull;
                {{ selectedWorksheet.columnCount || '?' }} столбцов
              </p>
            </div>

            <!-- Индикатор загрузки данных -->
            <div v-if="loadingSheetData" class="flex justify-center py-10">
              <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
            </div>

            <!-- Ошибка загрузки данных -->
            <div v-else-if="sheetDataError" class="bg-red-900/30 p-4 rounded-lg text-red-200 mb-6">
              {{ sheetDataError }}
            </div>

            <!-- Подсказка выбрать лист -->
            <div v-else-if="!selectedWorksheet" class="bg-gray-800 p-6 rounded-lg text-center">
              <svg class="w-16 h-16 text-gray-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
              <p class="text-gray-400">Выберите лист из боковой панели для просмотра данных</p>
            </div>

            <!-- Таблица с данными -->
            <div v-else-if="sheetData && sheetData.length > 0" class="overflow-x-auto">
              <div class="flex justify-end mb-4">
                <button
                  @click="refreshSheetData"
                  class="bg-blue-600 hover:bg-blue-700 text-white py-1 px-3 rounded-lg transition-colors text-sm flex items-center"
                >
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                  </svg>
                  Обновить данные
                </button>
              </div>

              <table class="min-w-full bg-gray-700 rounded-lg overflow-hidden">
                <thead class="bg-gray-600">
                  <tr>
                    <th
                      v-for="(cell, index) in sheetData[0]"
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

            <!-- Нет данных -->
            <div v-else-if="selectedWorksheet" class="bg-gray-800 p-6 rounded-lg text-center">
              <p class="text-gray-400">Нет данных в выбранном листе</p>
            </div>
          </div>
        </div>

        <!-- Секция подтверждения пользователей -->
        <div v-if="activeSection === 'approvals'">
          <div class="mb-6">
            <h2 class="text-2xl font-bold mb-4">Подтверждение пользователей</h2>
            <p class="text-gray-400 mb-6">Управление запросами на регистрацию</p>

            <!-- Индикатор загрузки -->
            <div v-if="loadingUsers" class="flex justify-center py-10">
              <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
            </div>

            <!-- Ошибка загрузки -->
            <div v-else-if="usersError" class="bg-red-900/30 p-4 rounded-lg text-red-200 mb-6">
              {{ usersError }}
            </div>

            <!-- Нет ожидающих подтверждения -->
            <div v-else-if="pendingUsers.length === 0" class="bg-gray-800 rounded-lg p-6 text-center text-gray-400">
              Нет ожидающих подтверждения пользователей
            </div>

            <!-- Список пользователей для подтверждения -->
            <div v-else class="space-y-4">
              <div v-for="user in pendingUsers" :key="user.id" class="bg-gray-800 rounded-lg p-4">
                <div class="flex justify-between items-center">
                  <div class="flex items-center">
                    <img
                      v-if="user.photo_url"
                      :src="user.photo_url"
                      alt="Фото профиля"
                      class="w-10 h-10 rounded-full mr-4"
                    >
                    <div v-else class="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center mr-4">
                      <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                      </svg>
                    </div>
                    <div>
                      <div class="font-medium">{{ user.first_name }} {{ user.last_name }}</div>
                      <div class="text-sm text-gray-400">{{ user.role || 'Роль не указана' }}</div>
                    </div>
                  </div>

                  <div class="flex space-x-3">
                    <button
                      @click="approveUser(user)"
                      class="bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg transition-colors"
                    >
                      Подтвердить
                    </button>
                    <button
                      @click="deleteUser(user)"
                      class="bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg transition-colors"
                    >
                      Отклонить
                    </button>
                  </div>
                </div>
              </div>

              <div class="mt-6 flex justify-end">
                <button
                  @click="fetchUsers"
                  class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition-colors flex items-center"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                  </svg>
                  Обновить список
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      user: null,
      activeSection: 'dashboard',

      // Список пользователей для подтверждения
      users: [],
      loadingUsers: false,
      usersError: null,

      // Google Sheets данные
      worksheets: [],
      loadingWorksheets: false,
      worksheetsError: null,
      selectedWorksheet: null,

      // Данные листа
      sheetData: [],
      loadingSheetData: false,
      sheetDataError: null,

      // ID таблицы Google Sheets
      spreadsheetId: '1qpyC0XzvTcKT6EISywvqESX3A0MwQoFDE8p-Bll4hps' // Пример ID
    }
  },
  computed: {
    roleName() {
      return this.user ? this.user.role : 'Загрузка...';
    },
    hasAdminAccess() {
      if (!this.user || !this.user.role) return false;

      const adminRoles = [
        'SITE_SUPPORT',
        'SITE_DEVELOPER',
        'SITE_FOUNDER',
        'Поддержка Сайта',
        'Разработчик Сайта',
        'Основатель Сайта'
      ];

      return adminRoles.includes(this.user.role);
    },
    pendingUsers() {
      return this.users.filter(user => !user.is_approved);
    }
  },
  methods: {
    async fetchUserData() {
      try {
        const token = localStorage.getItem('access_token');

        if (!token) {
          this.$router.push('/');
          return;
        }

        const response = await fetch('http://localhost:80/api/auth/me', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error('Ошибка при получении данных пользователя');
        }

        this.user = await response.json();

        // Если пользователь не подтвержден, перенаправляем на страницу ожидания
        if (!this.user.is_approved) {
          this.$router.push('/waiting-approval');
        }
      } catch (error) {
        console.error('Ошибка:', error);
        this.$router.push('/');
      }
    },

    async logout() {
      try {
        await fetch('http://localhost:80/api/auth/logout', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });

        localStorage.removeItem('access_token');
        this.$router.push('/');
      } catch (error) {
        console.error('Ошибка при выходе:', error);
      }
    },

    // Переключение на раздел Google Таблиц и загрузка данных
    async openGoogleSheets() {
      this.activeSection = 'tables';

      // Если листы еще не загружены, загружаем их
      if (this.worksheets.length === 0 && !this.loadingWorksheets) {
        await this.refreshWorksheets();
      }
    },

    // Переход на страницу администрирования
    navigateToAdmin() {
      this.$router.push('/admin');
    },

    // Методы для Google Sheets
    async refreshWorksheets() {
      this.loadingWorksheets = true;
      this.worksheetsError = null;

      try {
        // В реальном приложении здесь должен быть вызов API
        // Симулируем получение листов с сервера
        setTimeout(() => {
          this.worksheets = [
            { id: 'sheet1', title: 'Основной', rowCount: 100, columnCount: 10 },
            { id: 'sheet2', title: 'Тест1', rowCount: 50, columnCount: 5 },
            { id: 'sheet3', title: 'Тест2', rowCount: 20, columnCount: 8 }
          ];

          // Если нет выбранного листа и есть доступные листы, выбираем первый
          if (!this.selectedWorksheet && this.worksheets.length > 0) {
            this.selectWorksheet(this.worksheets[0]);
          }

          this.loadingWorksheets = false;
        }, 800); // Имитация задержки запроса
      } catch (error) {
        console.error('Ошибка при загрузке листов:', error);
        this.worksheetsError = `Ошибка при загрузке листов: ${error.message || 'Неизвестная ошибка'}`;
        this.loadingWorksheets = false;
      }
    },

    selectWorksheet(worksheet) {
      this.selectedWorksheet = worksheet;
      this.refreshSheetData();
    },

    async refreshSheetData() {
      if (!this.selectedWorksheet) return;

      this.loadingSheetData = true;
      this.sheetDataError = null;

      try {
        // Симуляция получения данных с сервера
        setTimeout(() => {
          // Генерируем тестовые данные в зависимости от выбранного листа
          if (this.selectedWorksheet.id === 'sheet1') {
            this.sheetData = [
              ['Имя', 'Фамилия', 'Email', 'Телефон', 'Дата регистрации'],
              ['Иван', 'Иванов', 'ivan@example.com', '+7(999)123-4567', '01.04.2025'],
              ['Петр', 'Петров', 'petr@example.com', '+7(999)765-4321', '02.04.2025'],
              ['Мария', 'Сидорова', 'maria@example.com', '+7(999)555-7777', '03.04.2025'],
              ['Алексей', 'Смирнов', 'alex@example.com', '+7(999)111-2222', '04.04.2025']
            ];
          } else if (this.selectedWorksheet.id === 'sheet3') {
            this.sheetData = [
              ['Категория', 'Название', 'Описание', 'Статус'],
              ['Задача', 'Разработка дашборда', 'Создание интерфейса для админ-панели', 'В процессе'],
              ['Баг', 'Ошибка авторизации', 'Проблема с токеном доступа', 'Исправлено'],
              ['Улучшение', 'Оптимизация запросов', 'Кэширование запросов к API', 'Запланировано']
            ];
          }

          this.loadingSheetData = false;
        }, 600); // Имитация задержки запроса
      } catch (error) {
        console.error('Ошибка при загрузке данных листа:', error);
        this.sheetDataError = `Ошибка при загрузке данных: ${error.message || 'Неизвестная ошибка'}`;
        this.loadingSheetData = false;
      }
    },

    // Методы для работы с пользователями
    async fetchUsers() {
      if (!this.hasAdminAccess) return;

      this.loadingUsers = true;
      this.usersError = null;

      try {
        const token = localStorage.getItem('access_token');

        // В реальном приложении здесь должен быть вызов API
        // Симулируем получение пользователей с сервера
        setTimeout(() => {
          this.users = [
            {
              id: 1,
              first_name: 'Алексей',
              last_name: 'Иванов',
              vk_id: '12345678',
              email: 'alexey@example.com',
              role: 'Пользователь',
              is_approved: false,
              photo_url: null
            },
            {
              id: 2,
              first_name: 'Екатерина',
              last_name: 'Смирнова',
              vk_id: '87654321',
              email: 'kate@example.com',
              role: 'Пользователь',
              is_approved: false,
              photo_url: null
            },
            {
              id: 3,
              first_name: 'Дмитрий',
              last_name: 'Петров',
              vk_id: '11223344',
              email: 'dmitry@example.com',
              role: 'Пользователь',
              is_approved: true,
              photo_url: null
            }
          ];

          this.loadingUsers = false;
        }, 700); // Имитация задержки запроса
      } catch (error) {
        console.error('Ошибка при получении списка пользователей:', error);
        this.usersError = `Ошибка при загрузке пользователей: ${error.message || 'Неизвестная ошибка'}`;
        this.loadingUsers = false;
      }
    },

    async approveUser(user) {
      if (!this.hasAdminAccess) return;

      try {
        const token = localStorage.getItem('access_token');

        // В реальном приложении здесь должен быть вызов API
        // Симулируем вызов API для подтверждения пользователя
        console.log(`Подтверждение пользователя ${user.id}`);

        // Обновляем статус пользователя локально для демонстрации
        const index = this.users.findIndex(u => u.id === user.id);
        if (index !== -1) {
          this.users[index].is_approved = true;
        }
      } catch (error) {
        console.error('Ошибка при подтверждении пользователя:', error);
        alert(`Ошибка при подтверждении пользователя: ${error.message || 'Неизвестная ошибка'}`);
      }
    },

    async deleteUser(user) {
      if (!this.hasAdminAccess) return;

      if (!confirm(`Вы уверены, что хотите удалить пользователя ${user.first_name} ${user.last_name}?`)) {
        return;
      }

      try {
        const token = localStorage.getItem('access_token');

        // В реальном приложении здесь должен быть вызов API
        // Симулируем вызов API для удаления пользователя
        console.log(`Удаление пользователя ${user.id}`);

        // Удаляем пользователя локально для демонстрации
        this.users = this.users.filter(u => u.id !== user.id);
      } catch (error) {
        console.error('Ошибка при удалении пользователя:', error);
        alert(`Ошибка при удалении пользователя: ${error.message || 'Неизвестная ошибка'}`);
      }
    }
  },
  mounted() {
    this.fetchUserData();

    // Если пользователь админ, загружаем пользователей
    if (this.hasAdminAccess) {
      this.fetchUsers();
    }
  }
}
</script>selectedWorksheet.id === 'sheet2') {
            this.sheetData = [
              ['Продукт', 'Цена', 'Количество', 'Сумма'],
              ['Товар А', '1000', '5', '5000'],
              ['Товар Б', '2000', '3', '6000'],
              ['Товар В', '500', '10', '5000']
            ];
          } else if (this.
