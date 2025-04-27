<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-gray-200 px-4">
    <!-- Лого и заголовок -->
    <div class="text-center mb-16">
      <h1 class="text-6xl md:text-7xl font-bold mb-4 bg-gradient-to-r from-gray-200 to-gray-400 text-transparent bg-clip-text tracking-tighter">
        Phantom Site
      </h1>
      <p class="text-gray-400 text-xl max-w-md mx-auto">
        Войдите, чтобы продолжить исследование
      </p>
    </div>

    <!-- Карточка входа -->
    <div class="w-full max-w-md">
      <div class="bg-gray-800 rounded-xl shadow-2xl shadow-gray-900/50 overflow-hidden p-8 transform transition-all hover:scale-[1.01]">
        <div class="mb-8 text-center">
          <div class="inline-block p-3 rounded-full bg-gray-700 mb-4">
            <svg class="w-8 h-8 text-gray-300" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-100">Авторизация</h2>
          <p class="text-gray-400 mt-2">Используйте ваш аккаунт ВКонтакте для входа</p>
        </div>

        <!-- Кнопка входа через ВК -->
        <button
          @click="login"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white py-4 px-6 rounded-lg shadow-lg font-medium flex items-center justify-center space-x-3 transition-all transform hover:translate-y-[-2px]"
        >
          <svg class="w-6 h-6" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <path d="M20.911 8.33268C21.0122 7.95003 20.911 7.66669 20.3778 7.66669H18.3778C17.9333 7.66669 17.7222 7.91114 17.6211 8.19448C17.6211 8.19448 16.5667 10.7334 15.0567 12.3778C14.6567 12.7778 14.4678 12.9111 14.2344 12.9111C14.1333 12.9111 13.9889 12.7778 13.9889 12.3945V8.33268C13.9889 7.88892 13.8567 7.66669 13.4789 7.66669H10.0789C9.79994 7.66669 9.63883 7.90003 9.63883 8.11669C9.63883 8.53336 10.3222 8.63892 10.3889 9.95558V12.9889C10.3889 13.5445 10.2789 13.6556 10.0456 13.6556C9.39994 13.6556 7.68327 11.1056 6.66661 8.36669C6.49994 7.88336 6.32217 7.66669 5.87772 7.66669H3.87772C3.37772 7.66669 3.26672 7.91114 3.26672 8.19448C3.26672 8.65558 3.91217 11.2 6.45005 14.5889C8.13339 16.9056 10.5 18.1667 12.6456 18.1667C13.9333 18.1667 14.0111 17.9111 14.0111 17.4834V15.6834C14.0111 15.1834 14.1278 15.0723 14.4789 15.0723C14.7567 15.0723 15.2 15.2056 16.4444 16.4C17.8444 17.8 18.0511 18.1667 18.7178 18.1667H20.7178C21.2178 18.1667 21.4733 17.9111 21.3389 17.4167C21.1889 16.9222 20.6233 16.2056 19.8678 15.3389C19.4678 14.8723 18.8678 14.3723 18.6789 14.0889C18.4011 13.7389 18.4678 13.5889 18.6789 13.2556C18.6789 13.2556 21.1778 9.82225 21.4011 8.33336L20.911 8.33268Z"/>
          </svg>
          <span>Войти через ВКонтакте</span>
        </button>

        <div class="mt-6 text-center text-gray-500 text-sm">
          Нажимая кнопку, вы соглашаетесь с условиями использования сайта
        </div>
      </div>
    </div>

    <!-- Декоративный элемент -->
    <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 via-indigo-500 to-blue-800"></div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  methods: {
    async login() {
      try {
        const response = await fetch('http://localhost:80/api/auth/vk/login');
        const data = await response.json();

        if (data.auth_url) {
          window.location.href = data.auth_url;
        }
      } catch (error) {
        console.error('Ошибка при получении URL авторизации:', error);
      }
    }
  }
}
</script>
