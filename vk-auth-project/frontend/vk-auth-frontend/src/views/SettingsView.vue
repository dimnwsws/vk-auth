<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">Настройки сайта</h2>

    <div class="space-y-6">
      <div class="bg-gray-700 rounded-lg p-6">
        <h3 class="text-xl font-semibold mb-4">Общие настройки</h3>

        <div class="space-y-4">
          <div>
            <label class="block text-gray-400 mb-2">Название сайта</label>
            <input
              type="text"
              v-model="settings.name"
              class="w-full bg-gray-600 text-gray-200 py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
          </div>

          <div>
            <label class="block text-gray-400 mb-2">Описание</label>
            <textarea
              v-model="settings.description"
              rows="3"
              class="w-full bg-gray-600 text-gray-200 py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            ></textarea>
          </div>

          <div>
            <label class="block text-gray-400 mb-2">Автоматическое подтверждение пользователей</label>
            <div class="flex items-center">
              <input
                type="checkbox"
                id="autoApprove"
                v-model="settings.autoApproveUsers"
                class="mr-2 h-4 w-4"
              >
              <label for="autoApprove">Включить автоматическое подтверждение</label>
            </div>
          </div>
        </div>

        <div class="mt-6">
          <button
            @click="saveSettings"
            class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-6 rounded-md transition-colors"
          >
            Сохранить настройки
          </button>
        </div>
      </div>

      <div class="bg-gray-700 rounded-lg p-6">
        <h3 class="text-xl font-semibold mb-4">Настройки безопасности</h3>

        <div class="space-y-4">
          <div>
            <label class="block text-gray-400 mb-2">Максимальное количество попыток входа</label>
            <input
              type="number"
              v-model="settings.maxLoginAttempts"
              min="1"
              max="10"
              class="w-full bg-gray-600 text-gray-200 py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
          </div>

          <div>
            <label class="block text-gray-400 mb-2">Время жизни сессии (минуты)</label>
            <input
              type="number"
              v-model="settings.sessionLifetime"
              min="5"
              max="1440"
              class="w-full bg-gray-600 text-gray-200 py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
          </div>
        </div>

        <div class="mt-6">
          <button
            @click="saveSecuritySettings"
            class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-6 rounded-md transition-colors"
          >
            Сохранить настройки безопасности
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SettingsView',
  props: {
    initialSettings: {
      type: Object,
      default() {
        return {
          name: 'Phantom Site',
          description: 'Современный сайт с авторизацией через ВКонтакте',
          autoApproveUsers: false,
          maxLoginAttempts: 5,
          sessionLifetime: 60
        }
      }
    }
  },
  data() {
    return {
      settings: { ...this.initialSettings }
    }
  },
  watch: {
    initialSettings: {
      handler(newVal) {
        this.settings = { ...newVal };
      },
      deep: true
    }
  },
  methods: {
    saveSettings() {
      this.$emit('save-settings', { ...this.settings });
    },
    saveSecuritySettings() {
      this.$emit('save-security-settings', {
        maxLoginAttempts: this.settings.maxLoginAttempts,
        sessionLifetime: this.settings.sessionLifetime
      });
    }
  }
}
</script>
