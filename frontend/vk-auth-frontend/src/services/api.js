// src/services/api.js
import axios from 'axios';

// Создание экземпляра axios с базовым URL
const api = axios.create({
  baseURL: 'http://localhost:80/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// Перехватчик для добавления токена к запросам
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token) {
      // Важно: используйте Bearer схему для JWT токенов
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// Перехватчик для обработки ошибок
api.interceptors.response.use(
  response => response,
  error => {
    // Если 401 (неавторизован), очищаем локальное хранилище и перенаправляем на страницу входа
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export default api;
