<template>
  <aside
    :class="[
      'bg-gray-800 shadow-lg transition-all duration-300 z-20',
      isMobileMenuOpen ? 'absolute inset-y-0 left-0 w-64 mt-14' : 'hidden md:block w-64'
    ]"
  >
    <div class="p-4">
      <div class="mb-6">
        <h2 class="text-lg font-semibold text-gray-300 mb-2">Панель управления</h2>
        <p class="text-xs text-gray-500">Phantom Site</p>
      </div>

      <!-- Основное меню -->
      <nav class="space-y-1">
        <router-link
          to="/dashboard"
          custom
          v-slot="{ isActive, navigate }"
        >
          <button
            @click="navigate"
            :class="[
              'w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors',
              isActive ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'
            ]"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zm10 0a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zm10 0a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path>
            </svg>
            <span>Обзор</span>
          </button>
        </router-link>

        <router-link
          to="/admin/users"
          custom
          v-slot="{ isActive, navigate }"
        >
          <button
            @click="navigate"
            :class="[
              'w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors',
              isActive ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'
            ]"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
            </svg>
            <span>Пользователи</span>
          </button>
        </router-link>

        <router-link
          to="/admin/approvals"
          custom
          v-slot="{ isActive, navigate }"
        >
          <button
            @click="navigate"
            :class="[
              'w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors',
              isActive ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'
            ]"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span class="flex-1">Запросы</span>
          </button>
        </router-link>

        <router-link
          to="/admin/settings"
          custom
          v-slot="{ isActive, navigate }"
        >
          <button
            @click="navigate"
            :class="[
              'w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors',
              isActive ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'
            ]"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
            </svg>
            <span>Настройки</span>
          </button>
        </router-link>

        <router-link
          to="/profile"
          custom
          v-slot="{ isActive, navigate }"
        >
          <button
            @click="navigate"
            :class="[
              'w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors',
              isActive ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'
            ]"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
            <span>Мой профиль</span>
          </button>
        </router-link>
      </nav>
    </div>
  </aside>
</template>

<script>
export default {
  name: 'SideBar',
  props: {
    isMobileMenuOpen: {
      type: Boolean,
      default: false
    }
  }
}
</script>
