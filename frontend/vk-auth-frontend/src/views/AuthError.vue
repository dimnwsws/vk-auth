<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900 text-gray-200">
    <div class="text-center">
      <div class="bg-gray-800 p-8 rounded-xl shadow-2xl max-w-md">
        <div class="flex justify-center">
          <div class="rounded-full bg-red-900/30 p-4">
            <svg class="w-16 h-16 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
        </div>
        <h2 class="mt-4 text-2xl font-semibold text-gray-100">Ошибка авторизации</h2>
        <p class="mt-2 text-gray-400">{{ errorMessage }}</p>
        <div class="mt-6">
          <router-link
            to="/"
            class="inline-block bg-gray-700 hover:bg-gray-600 text-white py-2 px-6 rounded-lg transition-colors">
            Вернуться на главную
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthError',
  data() {
    return {
      errorMessage: 'Произошла ошибка при авторизации через ВКонтакте. Пожалуйста, попробуйте снова.'
    }
  },
  mounted() {
    // Получаем сообщение об ошибке из URL, если оно есть
    const error = this.$route.query.error;
    if (error) {
      this.errorMessage = `Ошибка: ${error}`;
    }
  }
}
</script>
