<template>
  <nav class="bg-white shadow-md">
    <div class="container mx-auto px-4 py-4">
      <div class="flex justify-between items-center">
        <!-- Логотип -->
        <router-link to="/" class="flex items-center text-vk-blue font-bold text-2xl">
          <span class="mr-2">
            <svg class="w-8 h-8" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M26.8086 21.5664C26.6341 21.3086 26.1732 20.7432 24.9112 19.5489C23.5853 18.2968 23.7804 18.5177 25.3898 16.3633C26.359 15.0889 26.7873 14.318 26.643 13.9102C26.5054 13.5244 25.7939 13.6245 25.7939 13.6245L23.2246 13.6418C23.2246 13.6418 23.02 13.6135 22.8688 13.7057C22.7232 13.7959 22.6283 13.9995 22.6283 13.9995C22.6283 13.9995 22.2148 15.0452 21.6777 15.9316C20.5459 17.7972 20.0762 17.9073 19.8713 17.7739C19.3986 17.4685 19.5098 16.703 19.5098 16.1605C19.5098 14.3544 19.8008 13.4976 18.9756 13.2793C18.689 13.2046 18.4766 13.1548 17.9111 13.147C17.1948 13.1372 16.584 13.1514 16.2295 13.371C15.9976 13.5153 15.8203 13.8389 15.9658 13.8579C16.1465 13.8808 16.5444 13.9692 16.7109 14.2708C16.9287 14.6626 16.9189 15.3856 16.9189 15.3856C16.9189 15.3856 17.0732 17.4884 16.5732 17.7857C16.2324 17.9927 15.7607 17.6138 14.7559 15.9072C14.2402 15.0396 13.8389 14.0777 13.8389 14.0777C13.8389 14.0777 13.7568 13.8818 13.6133 13.7779C13.4365 13.652 13.1992 13.6117 13.1992 13.6117L10.7529 13.629C10.7529 13.629 10.3428 13.6394 10.2021 13.8045C10.0762 13.9515 10.1914 14.2557 10.1914 14.2557C10.1914 14.2557 12.0254 18.4375 14.0879 20.5523C15.9814 22.4971 18.1348 22.3613 18.1348 22.3613H19.0752C19.0752 22.3613 19.4165 22.3257 19.5908 22.1352C19.751 21.9586 19.7451 21.6558 19.7451 21.6558C19.7451 21.6558 19.7246 20.3845 20.3057 20.1582C20.876 19.9357 21.6191 21.4161 22.4043 21.9918C22.998 22.4302 23.4434 22.3359 23.4434 22.3359L25.7432 22.3613C25.7432 22.3613 26.8495 22.2827 26.335 21.5674L26.8086 21.5664Z" fill="#4C75A3"/>
              <path fill-rule="evenodd" clip-rule="evenodd" d="M16 30C23.732 30 30 23.732 30 16C30 8.26801 23.732 2 16 2C8.26801 2 2 8.26801 2 16C2 23.732 8.26801 30 16 30ZM16 32C24.8366 32 32 24.8366 32 16C32 7.16344 24.8366 0 16 0C7.16344 0 0 7.16344 0 16C0 24.8366 7.16344 32 16 32Z" fill="#4C75A3"/>
            </svg>
          </span>
          VK Auth
        </router-link>

        <!-- Навигация -->
        <div class="hidden md:flex items-center space-x-8">
          <router-link to="/" class="text-gray-600 hover:text-vk-blue transition">Главная</router-link>

          <!-- Кнопки авторизации -->
          <div v-if="!isAuthenticated">
            <button @click="login" class="bg-vk-blue text-white py-2 px-4 rounded-md hover:bg-vk-dark-blue transition">
              Войти через ВКонтакте
            </button>
          </div>

          <!-- Профиль пользователя -->
          <div v-else class="relative group">
            <div class="flex items-center cursor-pointer">
              <img v-if="user && user.photo_url" :src="user.photo_url" alt="Фото профиля" class="w-10 h-10 rounded-full mr-2">
              <span v-else class="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center mr-2">
                <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </span>
              <span class="text-gray-700">{{ userName }}</span>
            </div>

            <!-- Выпадающее меню -->
            <div class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10 hidden group-hover:block">
              <router-link to="/profile" class="block px-4 py-2 text-gray-700 hover:bg-gray-100">
                Мой профиль
              </router-link>
              <button @click="logout" class="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100">
                Выйти
              </button>
            </div>
          </div>
        </div>

        <!-- Мобильная навигация -->
        <div class="md:hidden">
          <button @click="toggleMobileMenu" class="text-gray-500 hover:text-vk-blue">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
      </div>

      <!-- Мобильное меню -->
      <div v-if="mobileMenuOpen" class="md:hidden mt-4 space-y-4">
        <router-link to="/" class="block text-gray-600 hover:text-vk-blue transition">Главная</router-link>

        <div v-if="!isAuthenticated" class="mt-4">
          <button @click="login" class="bg-vk-blue text-white py-2 px-4 rounded-md hover:bg-vk-dark-blue transition w-full">
            Войти через ВКонтакте
          </button>
        </div>

        <div v-else class="mt-4 space-y-2">
          <router-link to="/profile" class="block text-gray-600 hover:text-vk-blue transition">
            Мой профиль
          </router-link>
          <button @click="logout" class="block text-gray-600 hover:text-vk-blue transition">
            Выйти
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { useAuthStore } from '../stores/auth';

export default {
  name: 'Navbar',
  data() {
    return {
      mobileMenuOpen: false
    }
  },
  computed: {
    authStore() {
      return useAuthStore();
    },
    isAuthenticated() {
      return this.authStore.isAuthenticated;
    },
    user() {
      return this.authStore.user;
    },
    userName() {
      if (!this.user) return '';
      return `${this.user.first_name} ${this.user.last_name}`;
    }
  },
  methods: {
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen;
    },
    async login() {
      console.log("Attempting login via VK...");
      try {
        // Вызываем метод login из store
        await this.authStore.login();
      } catch (error) {
        console.error('Ошибка при входе:', error);
      }
    },
    async logout() {
      try {
        await this.authStore.logout();
        this.$router.push('/');
      } catch (error) {
        console.error('Ошибка при выходе:', error);
      }
    }
  },
  mounted() {
    this.authStore.initializeAuth();
  }
}
</script>
