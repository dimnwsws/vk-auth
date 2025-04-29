<template>
  <div class="min-h-screen bg-gray-900 text-gray-200">
    <!-- Верхняя панель навигации - такая же как в Dashboard -->
    <header class="bg-gray-800 shadow-md">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <h1 class="text-xl font-bold">Phantom Site - Административная панель</h1>

        <!-- Профиль пользователя -->
        <div class="relative group">
          <div class="flex items-center cursor-pointer">
            <img
              v-if="user && user.photo_url"
              :src="user.photo_url"
              alt="Фото профиля"
              class="w-10 h-10 rounded-full border-2 border-gray-700 transition-transform hover:scale-105"
            >
            <div v-else class="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center">
              <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </div>

            <!-- Выпадающее меню -->
            <div class="absolute right-0 top-12 w-56 bg-gray-800 rounded-lg shadow-xl py-2 z-50 hidden group-hover:block">
              <div class="px-4 py-2 border-b border-gray-700">
                <p class="font-medium">{{ user ? `${user.first_name} ${user.last_name}` : 'Загрузка...' }}</p>
                <p class="text-sm text-blue-400">{{ user ? user.role : 'Загрузка...' }}</p>
              </div>
              <router-link to="/dashboard" class="block px-4 py-2 hover:bg-gray-700 transition-colors">
                Панель управления
              </router-link>
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

    <!-- Основной контент -->
    <div class="container mx-auto px-4 py-8">
      <div class="flex mb-8">
        <!-- Боковое меню -->
        <div class="w-64 bg-gray-800 rounded-lg shadow-lg mr-6 p-4">
          <h2 class="text-xl font-bold mb-4 text-gray-200">Управление</h2>
          <ul class="space-y-2">
            <li>
              <button
                @click="activeTab = 'users'"
                :class="['w-full text-left px-4 py-2 rounded-md transition-colors',
                         activeTab === 'users' ? 'bg-blue-600 text-white' : 'hover:bg-gray-700']"
              >
                Пользователи
              </button>
            </li>
            <li>
              <button
                @click="activeTab = 'approvals'"
                :class="['w-full text-left px-4 py-2 rounded-md transition-colors',
                         activeTab === 'approvals' ? 'bg-blue-600 text-white' : 'hover:bg-gray-700']"
              >
                Запросы на подтверждение
                <span v-if="pendingUsers.length > 0" class="ml-2 bg-red-500 text-white px-2 py-0.5 rounded-full text-xs">
                  {{ pendingUsers.length }}
                </span>
              </button>
            </li>
            <li>
              <button
                @click="activeTab = 'settings'"
                :class="['w-full text-left px-4 py-2 rounded-md transition-colors',
                         activeTab === 'settings' ? 'bg-blue-600 text-white' : 'hover:bg-gray-700']"
              >
                Настройки сайта
              </button>
            </li>
          </ul>
        </div>

        <!-- Содержимое активной вкладки -->
        <div class="flex-1 bg-gray-800 rounded-lg shadow-lg p-6">
          <!-- Отображаем компоненты в зависимости от активной вкладки -->
          <users-view
            v-if="activeTab === 'users'"
            :users="users"
            :available-roles="availableRoles"
            @update-role="updateUserRole"
            @approve-user="approveUser"
            @delete-user="deleteUser"
          />

          <approvals-view
            v-else-if="activeTab === 'approvals'"
            :users="users"
            @approve-user="approveUser"
            @delete-user="deleteUser"
          />

          <settings-view
            v-else-if="activeTab === 'settings'"
            :initial-settings="siteSettings"
            @save-settings="saveSiteSettings"
            @save-security-settings="saveSecuritySettings"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UsersView from './UsersView.vue';
import ApprovalsView from './ApprovalsView.vue';
import SettingsView from './SettingsView.vue';

export default {
  name: 'AdminPanel',
  components: {
    UsersView,
    ApprovalsView,
    SettingsView
  },
  data() {
    return {
      user: null,
      activeTab: 'users',
      users: [],
      availableRoles: [
        'Гость',
        'Пользователь',
        'Заместитель организации',
        'Лидер организации',
        'Следящая администрация',
        'Заместитель Главного Следящего',
        'Главный Следящий',
        'Куратор',
        'Заместитель Главного администратора',
        'Главный администратор',
        'Поддержка Сайта',
        'Разработчик Сайта',
        'Основатель Сайта'
      ],
      siteSettings: {
        name: 'Phantom Site',
        description: 'Современный сайт с авторизацией через ВКонтакте',
        autoApproveUsers: false,
        maxLoginAttempts: 5,
        sessionLifetime: 60
      }
    }
  },
  computed: {
    pendingUsers() {
      return this.users.filter(user => !user.is_approved);
    },
    hasAdminAccess() {
      if (!this.user || !this.user.role) return false;

      const adminRoles = [
        'Поддержка Сайта',
        'Разработчик Сайта',
        'Основатель Сайта'
      ];

      return adminRoles.includes(this.user.role);
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

        // Проверка прав доступа
        if (!this.hasAdminAccess) {
          this.$router.push('/dashboard');
        }
      } catch (error) {
        console.error('Ошибка:', error);
        this.$router.push('/');
      }
    },
    async fetchUsers() {
      try {
        const token = localStorage.getItem('access_token');

        const response = await fetch('http://localhost:80/api/admin/users', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error('Ошибка при получении списка пользователей');
        }

        this.users = await response.json();
      } catch (error) {
        console.error('Ошибка:', error);
      }
    },
    async updateUserRole(user) {
      try {
        const token = localStorage.getItem('access_token');

        const response = await fetch(`http://localhost:80/api/admin/users/${user.id}/role`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ role: user.role })
        });

        if (!response.ok) {
          throw new Error('Ошибка при обновлении роли пользователя');
        }

        // Обновляем список пользователей
        this.fetchUsers();
      } catch (error) {
        console.error('Ошибка:', error);
      }
    },
    async approveUser(user) {
      try {
        const token = localStorage.getItem('access_token');

        const response = await fetch(`http://localhost:80/api/admin/users/${user.id}/approve`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error('Ошибка при подтверждении пользователя');
        }

        // Обновляем список пользователей
        this.fetchUsers();
      } catch (error) {
        console.error('Ошибка:', error);
      }
    },
    async deleteUser(user) {
      try {
        const token = localStorage.getItem('access_token');

        const response = await fetch(`http://localhost:80/api/admin/users/${user.id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error('Ошибка при удалении пользователя');
        }

        // Обновляем список пользователей
        this.fetchUsers();
      } catch (error) {
        console.error('Ошибка:', error);
      }
    },
    saveSiteSettings(settings) {
      this.siteSettings = { ...this.siteSettings, ...settings };
      // Здесь будет API-запрос для сохранения настроек на сервере
      console.log('Настройки сайта сохранены:', settings);
      // Показать уведомление об успешном сохранении
      alert('Настройки сайта успешно сохранены');
    },
    saveSecuritySettings(securitySettings) {
      this.siteSettings = { ...this.siteSettings, ...securitySettings };
      // Здесь будет API-запрос для сохранения настроек безопасности на сервере
      console.log('Настройки безопасности сохранены:', securitySettings);
      // Показать уведомление об успешном сохранении
      alert('Настройки безопасности успешно сохранены');
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
    }
  },
  async mounted() {
    await this.fetchUserData();
    await this.fetchUsers();
  }
}
</script>
