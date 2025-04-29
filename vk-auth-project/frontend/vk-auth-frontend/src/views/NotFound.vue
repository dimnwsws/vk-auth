<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900 text-gray-200">
    <div class="text-center">
      <div class="bg-gray-800 p-8 rounded-xl shadow-2xl max-w-md">
        <h1 class="text-6xl font-bold text-gray-100">404</h1>
        <h2 class="mt-4 text-2xl font-semibold text-gray-200">Страница не найдена</h2>
        <p class="mt-2 text-gray-400">Страница, которую вы ищете, не существует или была перемещена.</p>
        <div class="mt-6">
          <router-link
            to="/"
            class="inline-block bg-blue-600 hover:bg-blue-700 text-white py-2 px-6 rounded-lg transition-colors">
            Вернуться на главную
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>
