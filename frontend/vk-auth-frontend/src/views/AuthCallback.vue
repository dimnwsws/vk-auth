<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900">
    <div class="text-center">
      <div class="bg-gray-800 p-8 rounded-xl shadow-2xl max-w-md">
        <div class="flex justify-center">
          <svg class="animate-spin h-16 w-16 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
        <h2 class="mt-4 text-2xl font-semibold text-gray-100">Авторизация...</h2>
        <p class="mt-2 text-gray-400">Пожалуйста, подождите, пока мы обрабатываем ваш вход.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthCallback',
  mounted() {
    console.log("AuthCallback component mounted");
    // Получение query параметров из URL
    const token = this.$route.query.token;
    const userId = this.$route.query.user_id;

    console.log("Token from URL:", token);

    if (token) {
      // Сохранение токена в localStorage
      localStorage.setItem('access_token', token);
      console.log("Token saved to localStorage");

      // Перенаправление на дашборд вместо профиля
      this.$router.push('/dashboard');
    } else {
      // Ошибка авторизации
      console.error("No token received");
      this.$router.push('/auth-error');
    }
  }
}
</script>
