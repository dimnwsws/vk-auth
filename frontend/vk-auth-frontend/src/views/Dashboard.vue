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

    <!-- Основной контент -->
    <main class="container mx-auto px-4 py-8">
      <div class="mb-8">
        <h2 class="text-2xl font-bold mb-4">Добро пожаловать, {{ user ? user.first_name : 'Пользователь' }}!</h2>
        <p class="text-gray-400">Ваш статус: <span class="text-blue-400 font-medium">{{ roleName }}</span></p>
      </div>

      <!-- Карточки функций -->
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

        <!-- В секции с карточками функций -->
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
    </main>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      user: null
    }
  },
  computed: {
    roleName() {
      return this.user ? this.user.role : 'Загрузка...';
    },
    hasAdminAccess() {
      if (!this.user || !this.user.role) return false;

      const adminRoles = [
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
    }
  },
  mounted() {
    this.fetchUserData();
  }
}
</script>
