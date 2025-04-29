<template>
  <div class="min-h-screen w-full bg-gray-900 text-gray-200">
    <!-- Верхний градиентный баннер -->
    <div class="h-40 sm:h-48 bg-gradient-to-r from-gray-800 to-gray-700 relative w-full">
      <div class="absolute bottom-0 left-0 w-full overflow-hidden">
        <svg preserveAspectRatio="none" width="100%" height="74" viewBox="0 0 1440 74" class="w-full text-gray-900 fill-current">
          <path d="M456.464 0.0433865C277.158 -1.70575 0 50.0141 0 50.0141V74H1440V50.0141C1440 50.0141 1320.4 31.1925 1243.09 27.0276C1099.33 19.2816 1019.08 53.1981 875.138 50.0141C710.527 46.3727 621.108 1.64949 456.464 0.0433865Z"></path>
        </svg>
      </div>
    </div>

    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-6 -mt-24 relative z-10 h-[calc(100vh-48px)]">
      <!-- Карточка профиля -->
      <div class="bg-gray-800 rounded-xl shadow-2xl p-6 md:p-8 mb-6">
        <div class="flex flex-col md:flex-row items-center md:items-start gap-6 md:gap-8">
          <!-- Аватар -->
          <div class="mb-4 md:mb-0 flex-shrink-0">
            <img v-if="user && user.photo_url" :src="user.photo_url" alt="Фото профиля"
                 class="w-28 h-28 sm:w-32 sm:h-32 rounded-full border-4 border-gray-700 shadow-lg">
            <div v-else class="w-28 h-28 sm:w-32 sm:h-32 rounded-full bg-gray-700 flex items-center justify-center">
              <svg class="w-14 h-14 sm:w-16 sm:h-16 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </div>
          </div>

          <!-- Данные профиля -->
          <div class="text-center md:text-left flex-1">
            <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-100 mb-2">{{ fullName }}</h1>
            <p class="text-blue-400 mb-1">ID: {{ user ? user.vk_id : 'Загрузка...' }}</p>
            <p class="text-green-400 mb-4">{{ displayedRole }}</p>

            <div class="flex flex-wrap justify-center md:justify-start gap-3 md:gap-4">
              <div class="bg-gray-700 px-4 py-2 rounded-lg">
                <div class="text-gray-400 text-xs sm:text-sm">Профиль создан</div>
                <div class="font-medium text-sm sm:text-base">{{ formattedCreatedAt }}</div>
              </div>

              <div class="bg-gray-700 px-4 py-2 rounded-lg">
                <div class="text-gray-400 text-xs sm:text-sm">Последний вход</div>
                <div class="font-medium text-sm sm:text-base">{{ lastLoginTime }}</div>
              </div>

              <div class="bg-gray-700 px-4 py-2 rounded-lg">
                <div class="text-gray-400 text-xs sm:text-sm">Статус</div>
                <div class="font-medium text-sm sm:text-base text-green-400">Активный</div>
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

      <!-- Информационные карточки - заполняют все доступное пространство -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 h-[calc(100%-220px)]">
        <div class="bg-gray-800 rounded-xl shadow-lg p-6 h-full">
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
            <div class="flex justify-between">
              <span class="text-gray-400">ID ВКонтакте:</span>
              <span>{{ user ? user.vk_id : 'Загрузка...' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">Роль:</span>
              <span>{{ displayedRole }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">Подтверждение:</span>
              <span class="text-green-400">{{ user && user.is_approved ? 'Подтвержден' : 'Не подтвержден' }}</span>
            </div>
          </div>
        </div>

        <div class="bg-gray-800 rounded-xl shadow-lg p-6 h-full">
          <h2 class="text-xl font-bold mb-4 text-gray-100">Дополнительная информация</h2>
          <div class="space-y-4">
            <div>
              <p class="text-gray-400 mb-2">Ваша учетная запись успешно подтверждена и активирована в системе.</p>
              <p class="text-gray-400">Используйте панель управления для доступа к функциям системы в соответствии с вашим уровнем доступа.</p>
            </div>

            <div class="mt-6">
              <button @click="goToDashboard" class="w-full bg-blue-600 hover:bg-blue-700 py-2 px-4 rounded-lg mb-4 transition-colors">
                Перейти в панель управления
              </button>
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
      error: null,
      roleTranslations: {
        'GUEST': 'Гость',
        'USER': 'Пользователь',
        'ORG_DEPUTY': 'Заместитель организации',
        'ORG_LEADER': 'Лидер организации',
        'ADMIN_OBSERVER': 'Следящая администрация',
        'CHIEF_OBSERVER_DEPUTY': 'Заместитель Главного Следящего',
        'CHIEF_OBSERVER': 'Главный Следящий',
        'CURATOR': 'Куратор',
        'CHIEF_ADMIN_DEPUTY': 'Заместитель Главного администратора',
        'CHIEF_ADMIN': 'Главный администратор',
        'SITE_SUPPORT': 'Поддержка Сайта',
        'SITE_DEVELOPER': 'Разработчик Сайта',
        'SITE_FOUNDER': 'Основатель Сайта'
      }
    }
  },
  computed: {
    fullName() {
      if (!this.user) return 'Загрузка...';
      return `${this.user.first_name} ${this.user.last_name}`;
    },
    displayedRole() {
      if (!this.user || !this.user.role) return 'Загрузка...';

      // Если роль уже переведена, используем ее напрямую
      if (!this.user.role.startsWith('SITE_') &&
          !this.user.role.startsWith('CHIEF_') &&
          !this.user.role.startsWith('ORG_') &&
          !this.user.role.startsWith('ADMIN_')) {
        return this.user.role;
      }

      // Иначе ищем перевод
      return this.roleTranslations[this.user.role] || this.user.role;
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
    goToDashboard() {
      this.$router.push('/dashboard');
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
