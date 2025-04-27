// src/stores/auth.js
import { defineStore } from 'pinia';
import authService from '../services/auth';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    isLoading: false,
    error: null
  }),

  actions: {
    /**
     * Инициировать вход через ВКонтакте
     */
    async login() {
      this.isLoading = true;
      this.error = null;

      try {
        console.log("Fetching VK auth URL...");
        const data = await authService.getAuthUrl();
        console.log("Received auth URL:", data.auth_url);

        // Редирект на страницу авторизации ВК
        window.location.href = data.auth_url;
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка при авторизации';
        console.error('Login error:', error);
      } finally {
        this.isLoading = false;
      }
    },

    /**
     * Получить данные текущего пользователя
     */
    async fetchCurrentUser() {
      this.isLoading = true;
      this.error = null;

      try {
        // Проверяем наличие токена
        const token = localStorage.getItem('access_token');
        if (!token) {
          this.isAuthenticated = false;
          this.user = null;
          return;
        }

        // Получаем данные пользователя
        const user = await authService.getCurrentUser();
        this.user = user;
        this.isAuthenticated = true;

        // Сохраняем в localStorage для последующего использования
        localStorage.setItem('user', JSON.stringify(user));
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка при получении данных пользователя';
        this.isAuthenticated = false;
        this.user = null;
        console.error('Fetch user error:', error);
      } finally {
        this.isLoading = false;
      }
    },

    /**
     * Выход из системы
     */
    async logout() {
      this.isLoading = true;
      this.error = null;

      try {
        await authService.logout();
        this.user = null;
        this.isAuthenticated = false;
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка при выходе из системы';
        console.error('Logout error:', error);
      } finally {
        this.isLoading = false;
      }
    },

    /**
     * Восстановление сессии из localStorage
     */
    initializeAuth() {
      const token = localStorage.getItem('access_token');
      const userStr = localStorage.getItem('user');

      if (token && userStr) {
        try {
          this.user = JSON.parse(userStr);
          this.isAuthenticated = true;
        } catch (e) {
          console.error('Ошибка при разборе данных пользователя:', e);
          localStorage.removeItem('user');
        }
      }
    }
  }
});
