<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900 text-gray-200 px-4">
    <div class="max-w-md w-full bg-gray-800 rounded-xl shadow-2xl p-8 text-center">
      <div class="flex justify-center mb-6">
        <div class="rounded-full bg-yellow-600/30 p-4">
          <svg class="w-12 h-12 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
      </div>

      <h1 class="text-2xl font-bold mb-4">Ожидание подтверждения</h1>
      <p class="text-gray-400 mb-6">
        Ваша учетная запись ожидает подтверждения администратором.
        Пожалуйста, проверьте статус позже.
      </p>

      <div class="bg-gray-700 rounded-lg p-4 mb-6">
        <div class="flex items-center mb-2">
          <img v-if="user && user.photo_url" :src="user.photo_url" alt="Фото профиля" class="w-10 h-10 rounded-full mr-3">
          <div v-else class="w-10 h-10 rounded-full bg-gray-600 flex items-center justify-center mr-3">
            <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
          </div>
          <div class="text-left">
            <p class="font-medium">{{ user ? `${user.first_name} ${user.last_name}` : 'Загрузка...' }}</p>
            <p class="text-sm text-gray-400">{{ user ? `ID: ${user.vk_id}` : '' }}</p>
          </div>
        </div>
      </div>

      <button @click="checkStatus" class="w-full bg-blue-600 hover:bg-blue-700 py-2 px-4 rounded-lg mb-4 transition-colors">
        Проверить статус
      </button>

      <button @click="logout" class="w-full bg-gray-700 hover:bg-gray-600 py-2 px-4 rounded-lg transition-colors">
        Выйти из аккаунта
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WaitingApproval',
  data() {
    return {
      user: null
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

        // Если пользователь уже подтвержден, перенаправляем на дашборд
        if (this.user.is_approved) {
          this.$router.push('/dashboard');
        }
      } catch (error) {
        console.error('Ошибка:', error);
      }
    },
    async checkStatus() {
      // Перепроверяем статус пользователя
      await this.fetchUserData();
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
