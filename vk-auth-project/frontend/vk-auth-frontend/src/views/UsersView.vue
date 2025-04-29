<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">Управление пользователями</h2>

    <div class="mb-4 flex items-center">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Поиск пользователей..."
        class="bg-gray-700 text-gray-200 py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 flex-grow"
      >
      <select
        v-model="roleFilter"
        class="ml-4 bg-gray-700 text-gray-200 py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">Все роли</option>
        <option v-for="role in availableRoles" :key="role" :value="role">{{ role }}</option>
      </select>
    </div>

    <!-- Таблица пользователей -->
    <div class="overflow-x-auto">
      <table class="w-full border-collapse">
        <thead>
          <tr class="bg-gray-700 text-left">
            <th class="p-3 rounded-tl-lg">ID</th>
            <th class="p-3">Пользователь</th>
            <th class="p-3">Роль</th>
            <th class="p-3">Статус</th>
            <th class="p-3 rounded-tr-lg">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id" class="border-b border-gray-700">
            <td class="p-3">{{ user.id }}</td>
            <td class="p-3">
              <div class="flex items-center">
                <img
                  v-if="user.photo_url"
                  :src="user.photo_url"
                  class="w-8 h-8 rounded-full mr-3"
                  alt="Фото профиля"
                >
                <div>
                  {{ user.first_name }} {{ user.last_name }}
                  <div class="text-sm text-gray-400">{{ user.email || 'Email не указан' }}</div>
                </div>
              </div>
            </td>
            <td class="p-3">
              <select
                v-model="user.role"
                class="bg-gray-700 text-gray-200 py-1 px-2 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                @change="updateUserRole(user)"
              >
                <option v-for="role in availableRoles" :key="role" :value="role">{{ role }}</option>
              </select>
            </td>
            <td class="p-3">
              <span :class="[
                'px-2 py-1 rounded-full text-xs',
                user.is_approved ? 'bg-green-900 text-green-200' : 'bg-yellow-900 text-yellow-200'
              ]">
                {{ user.is_approved ? 'Подтвержден' : 'Ожидает подтверждения' }}
              </span>
            </td>
            <td class="p-3">
              <div class="flex space-x-2">
                <button
                  v-if="!user.is_approved"
                  @click="approveUser(user)"
                  class="bg-green-600 hover:bg-green-700 text-white py-1 px-3 rounded-md text-sm transition-colors"
                >
                  Подтвердить
                </button>
                <button
                  class="bg-red-600 hover:bg-red-700 text-white py-1 px-3 rounded-md text-sm transition-colors"
                  @click="deleteUser(user)"
                >
                  Удалить
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UsersView',
  props: {
    users: {
      type: Array,
      required: true
    },
    availableRoles: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      searchQuery: '',
      roleFilter: ''
    }
  },
  computed: {
    filteredUsers() {
      return this.users.filter(user => {
        const matchesSearch =
          !this.searchQuery ||
          user.first_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          user.last_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          (user.email && user.email.toLowerCase().includes(this.searchQuery.toLowerCase()));

        const matchesRole = !this.roleFilter || user.role === this.roleFilter;

        return matchesSearch && matchesRole;
      });
    }
  },
  methods: {
    updateUserRole(user) {
      this.$emit('update-role', user);
    },
    approveUser(user) {
      this.$emit('approve-user', user);
    },
    deleteUser(user) {
      if (confirm(`Вы уверены, что хотите удалить пользователя ${user.first_name} ${user.last_name}?`)) {
        this.$emit('delete-user', user);
      }
    }
  }
}
</script>
