// src/services/auth.js
import api from './api';

export default {
  /**
   * Получить URL авторизации ВКонтакте
   */
  async getAuthUrl() {
    try {
      const response = await api.get('/auth/vk/login');
      return response.data;
    } catch (error) {
      console.error('Ошибка при получении URL авторизации:', error);
      throw error;
    }
  },

  /**
   * Получить информацию о текущем пользователе
   */
  async getCurrentUser() {
    try {
      const response = await api.get('/auth/me');
      return response.data;
    } catch (error) {
      console.error('Ошибка при получении информации о пользователе:', error);
      throw error;
    }
  },

  /**
   * Выйти из системы
   */
  async logout() {
    try {
      await api.post('/auth/logout');
      // Очистить локальное хранилище
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
    } catch (error) {
      console.error('Ошибка при выходе из системы:', error);
      throw error;
    }
  }
};
