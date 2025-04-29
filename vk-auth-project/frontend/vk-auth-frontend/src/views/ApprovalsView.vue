<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">Запросы на подтверждение</h2>

    <div v-if="pendingUsers.length === 0" class="text-center py-8 text-gray-400">
      Нет ожидающих подтверждения пользователей
    </div>

    <div v-else class="space-y-4">
      <div v-for="user in pendingUsers" :key="user.id" class="bg-gray-700 rounded-lg p-4 flex justify-between items-center">
        <div class="flex items-center">
          <img
            v-if="user.photo_url"
            :src="user.photo_url"
            class="w-10 h-10 rounded-full mr-4"
            alt="Фото профиля"
          >
          <div v-else class="w-10 h-10 bg-gray-600 rounded-full flex items-center justify-center mr-4">
            <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
          </div>
          <div>
            <div class="font-medium">{{ user.first_name }} {{ user.last_name }}</div>
            <div class="text-sm text-gray-400">{{ user.email || 'Email не указан' }}</div>
            <div class="text-sm text-blue-400">ID ВКонтакте: {{ user.vk_id }}</div>
            <div class="text-sm text-gray-400">Создан: {{ formatDate(user.created_at) }}</div>
          </div>
        </div>

        <div class="flex space-x-3">
          <button
            @click="approveUser(user)"
            class="bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-md transition-colors"
          >
            Подтвердить
          </button>
          <button
            @click="deleteUser(user)"
            class="bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-md transition-colors"
          >
            Отклонить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ApprovalsView',
  props: {
    users: {
      type: Array,
      required: true
    }
  },
  computed: {
    pendingUsers() {
      return this.users.filter(user => !user.is_approved);
    }
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return 'Неизвестно';
      return new Date(dateString).toLocaleDateString();
    },
    approveUser(user) {
      this.$emit('approve-user', user);
    },
    deleteUser(user) {
      if (confirm(`Вы уверены, что хотите отклонить пользователя ${user.first_name} ${user.last_name}?`)) {
        this.$emit('delete-user', user);
      }
    }
  }
}
</script>
