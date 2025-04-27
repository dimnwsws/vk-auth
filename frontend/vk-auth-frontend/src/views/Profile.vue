<template>
  <div class="min-h-screen bg-gray-900 text-gray-200">
    <!-- Верхний градиентный баннер -->
    <div class="h-48 bg-gradient-to-r from-gray-800 to-gray-700 relative">
      <div class="absolute bottom-0 left-0 w-full overflow-hidden">
        <svg preserveAspectRatio="none" width="1440" height="74" viewBox="0 0 1440 74" class="w-full text-gray-900 fill-current">
          <path d="M456.464 0.0433865C277.158 -1.70575 0 50.0141 0 50.0141V74H1440V50.0141C1440 50.0141 1320.4 31.1925 1243.09 27.0276C1099.33 19.2816 1019.08 53.1981 875.138 50.0141C710.527 46.3727 621.108 1.64949 456.464 0.0433865Z"></path>
        </svg>
      </div>
    </div>

    <div class="container mx-auto px-4 py-8 -mt-32 relative z-10">
      <!-- Карточка профиля -->
      <div class="bg-gray-800 rounded-xl shadow-2xl p-8 mb-8">
        <div class="flex flex-col md:flex-row items-center md:items-start md:space-x-8">
          <!-- Аватар -->
          <div class="mb-6 md:mb-0">
            <img v-if="user && user.photo_url" :src="user.photo_url" alt="Фото профиля"
                 class="w-32 h-32 rounded-full border-4 border-gray-700 shadow-lg">
            <div v-else class="w-32 h-32 rounded-full bg-gray-700 flex items-center justify-center">
              <svg class="w-16 h-16 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </div>
          </div>

          <!-- Данные профиля -->
          <div class="text-center md:text-left">
            <h1 class="text-3xl font-bold text-gray-100 mb-2">{{ fullName }}</h1>
            <p class="text-blue-400 mb-1">ID: {{ user ? user.vk_id : 'Загрузка...' }}</p>
            <p class="text-green-400 mb-4">{{ user ? user.role : 'Загрузка...' }}</p>

            <div class="flex flex-wrap justify-center md:justify-start gap-4">
              <div class="bg-gray-700 px-4 py-2 rounded-lg">
                <div class="text-gray-400 text-sm">Профиль создан</div>
                <div class="font-medium">{{ formattedCreatedAt }}</div>
              </div>

              <div class="bg-gray-700 px-4 py-2 rounded-lg">
                <div class="text-gray-400 text-sm">Последний вход</div>
                <div class="font-medium">{{ lastLoginTime }}</div>
              </div>

              <div class="bg-gray-700 px-4 py-2 rounded-lg">
                <div class="text-gray-400 text-sm">Статус</div>
                <div class="font-medium text-green-400">Активный</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Действия -->
        <div class="mt-8 flex justify-center md:justify-start">
          <button @click="logout"
                  class="bg-red-600 hover:bg-red-700 text-white py-2 px-6 rounded-lg shadow transition-all">
            Выйти из аккаунта
          </button>
        </div>
      </div>

      <!-- Дополнительная информация -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-gray-800 rounded-xl shadow-lg p-6">
          <h2 class="text-xl font-bold mb-4 text-gray-100">Информация о профиле</h2>
          <div class="space-y-3">
            <div class="flex justify-between">
              <span class="text-gray-400">Имя:</span>
              <span>{{ user ? user.first_name : 'Загрузка...' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">Фамилия:</span>
              <span>{{ user ? user.last_name : 'Загрузка...' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">Email:</span>
              <span>{{ user && user.email ? user.email : 'Не указан' }}</span>
            </div>
          </div>
        </div>

        <div class="bg-gray-800 rounded-xl shadow-lg p-6">
          <h2 class="text-xl font-bold mb-4 text-gray-100">Статистика активности</h2>
          <div class="space-y-3">
            <div class="w-full bg-gray-700 rounded-full h-4">
              <div class="bg-blue-600 h-4 rounded-full" style="width: 75%"></div>
            </div>
            <div class="text-sm text-gray-400">
              75% заполненности профиля
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  data() {
    return {
      user: null,
      loading: true,
      error: null
    }
  },
  computed: {
    fullName() {
      if (!this.user) return 'Загрузка...';
      return `${this.user.first_name} ${this.user.last_name}`;
    },
    formattedCreatedAt() {
      if (!this.user || !this.user.created_at) return 'Неизвестно';
      return new Date(this.user.created_at).toLocaleDateString();
    },
    lastLoginTime() {
      if (!this.user || !this.user.updated_at) return 'Неизвестно';
      return new Date(this.user.updated_at).toLocaleString();
    }
  },
  methods: {
    async fetchUserData() {
      try {
        this.loading = true;
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
      } catch (error) {
        console.error('Ошибка:', error);
        this.error = error.message;
      } finally {
        this.loading = false;
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
