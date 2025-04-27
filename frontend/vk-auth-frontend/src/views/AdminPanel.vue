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
                         activeTab === 'users' ? 'bg-vk-blue text-white' : 'hover:bg-gray-700']"
              >
                Пользователи
              </button>
            </li>
            <li>
              <button
                @click="activeTab = 'approvals'"
                :class="['w-full text-left px-4 py-2 rounded-md transition-colors',
                         activeTab === 'approvals' ? 'bg-vk-blue text-white' : 'hover:bg-gray-700']"
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
                         activeTab === 'settings' ? 'bg-vk-blue text-white' : 'hover:bg-gray-700']"
              >
                Настройки сайта
              </button>
            </li>
          </ul>
        </div>

        <!-- Содержимое активной вкладки -->
        <div class="flex-1 bg-gray-800 rounded-lg shadow-lg p-6">
          <!-- Пользователи -->
          <div v-if="activeTab === 'users'">
            <h2 class="text-2xl font-bold mb-6">Управление пользователями</h2>

            <div class="mb-4 flex items-center">
              <input
                type="text"
                v-model="searchQuery"
                placeholder="Поиск пользователей..."
                class="bg-gray-700 text-gray-200 py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 flex-grow"
              >
              <select
                v-model="roleFilter"
                class="ml-4 bg-gray-700 text-gray-200 py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Все роли</option>
                <option v-for="role in availableRoles" :key="role" :value="role">{{ role }}</option>
              </select>
            </div>

            <!-- Таблица пользователей -->
            <div class="overflow-x-auto">
              <table class="w-full border-collapse">
                <thead>
                  <tr class="bg-gray-700 text-left">
                    <th class="p-3 rounded-tl-lg">ID</th>
                    <th class="p-3">Пользователь</th>
                    <th class="p-3">Роль</th>
                    <th class="p-3">Статус</th>
                    <th class="p-3 rounded-tr-lg">Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in filteredUsers" :key="user.id" class="border-b border-gray-700">
                    <td class="p-3">{{ user.id }}</td>
                    <td class="p-3">
                      <div class="flex items-center">
                        <img
                          v-if="user.photo_url"
                          :src="user.photo_url"
                          class="w-8 h-8 rounded-full mr-3"
                          alt="Фото профиля"
                        >
                        <div>
                          {{ user.first_name }} {{ user.last_name }}
                          <div class="text-sm text-gray-400">{{ user.email || 'Email не указан' }}</div>
                        </div>
                      </div>
                    </td>
                    <td class="p-3">
                      <select
                        v-model="user.role"
                        class="bg-gray-700 text-gray-200 py-1 px-2 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                        @change="updateUserRole(user)"
                      >
                        <option v-for="role in availableRoles" :key="role" :value="role">{{ role }}</option>
                      </select>
                    </td>
                    <td class="p-3">
                      <span :class="[
                        'px-2 py-1 rounded-full text-xs',
                        user.is_approved ? 'bg-green-900 text-green-200' : 'bg-yellow-900 text-yellow-200'
                      ]">
                        {{ user.is_approved ? 'Подтвержден' : 'Ожидает подтверждения' }}
                      </span>
                    </td>
                    <td class="p-3">
                      <div class="flex space-x-2">
                        <button
                          v-if="!user.is_approved"
                          @click="approveUser(user)"
                          class="bg-green-600 hover:bg-green-700 text-white py-1 px-3 rounded-md text-sm transition-colors"
                        >
                          Подтвердить
                        </button>
                        <button
                          class="bg-red-600 hover:bg-red-700 text-white py-1 px-3 rounded-md text-sm transition-colors"
                          @click="deleteUser(user)"
                        >
                          Удалить
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Запросы на подтверждение -->
          <div v-else-if="activeTab === 'approvals'">
            <h2 class="text-2xl font-bold mb-6">Запросы на подтверждение</h2>

            <div v-if="pendingUsers.length === 0" class="text-center py-8 text-gray-400">
              Нет ожидающих подтверждения пользователей
            </div>

            <div v-else class="space-y-4">
              <div v-for="user in pendingUsers" :key="user.id" class="bg-gray-700 rounded-lg p-4 flex justify-between items-center">
                <div class="flex items-center">
                  <img
                    v-if="user.photo_url"
                    :src="user.photo_url"
                    class="w-10 h-10 rounded-full mr-4"
                    alt="Фото профиля"
                  >
                  <div>
                    <div class="font-medium">{{ user.first_name }} {{ user.last_name }}</div>
                    <div class="text-sm text-gray-400">{{ user.email || 'Email не указан' }}</div>
                  </div>
                </div>

                <div class="flex space-x-3">
                  <button
                    @click="approveUser(user)"
                    class="bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-md transition-colors"
                  >
                    Подтвердить
                  </button>
                  <button
                    @click="deleteUser(user)"
                    class="bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-md transition-colors"
                  >
                    Отклонить
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Настройки сайта -->
          <div v-else-if="activeTab === 'settings'">
            <h2 class="text-2xl font-bold mb-6">Настройки сайта</h2>

            <div class="space-y-6">
              <div class="bg-gray-700 rounded-lg p-6">
                <h3 class="text-xl font-semibold mb-4">Общие настройки</h3>

                <div class="space-y-4">
                  <div>
                    <label class="block text-gray-400 mb-2">Название сайта</label>
                    <input
                      type="text"
                      v-model="siteSettings.name"
                      class="w-full bg-gray-600 text-gray-200 py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>

                  <div>
                    <label class="block text-gray-400 mb-2">Описание</label>
                    <textarea
                      v-model="siteSettings.description"
                      rows="3"
                      class="w-full bg-gray-600 text-gray-200 py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    ></textarea>
                  </div>

                  <div>
                    <label class="block text-gray-400 mb-2">Автоматическое подтверждение пользователей</label>
                    <div class="flex items-center">
                      <input
                        type="checkbox"
                        id="autoApprove"
                        v-model="siteSettings.autoApproveUsers"
                        class="mr-2 h-4 w-4"
                      >
                      <label for="autoApprove">Включить автоматическое подтверждение</label>
                    </div>
                  </div>
                </div>

                <div class="mt-6">
                  <button class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-6 rounded-md transition-colors">
                    Сохранить настройки
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminPanel',
  data() {
    return {
      user: null,
      activeTab: 'users',
      users: [],
      searchQuery: '',
      roleFilter: '',
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
        autoApproveUsers: false
      }
    }
  },
  computed: {
    filteredUsers() {
      return this.users.filter(user => {
        const matchesSearch =
          !this.searchQuery ||
          user.first_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          user.last_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          (user.email && user.email.toLowerCase().includes(this.searchQuery.toLowerCase()));

        const matchesRole = !this.roleFilter || user.role === this.roleFilter;

        return matchesSearch && matchesRole;
      });
    },
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
      if (!confirm(`Вы уверены, что хотите удалить пользователя ${user.first_name} ${user.last_name}?`)) {
        return;
      }

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
