<template>
  <a-layout id="app-layout">
    <a-layout-header class="app-header">
      <div class="app-logo">SiliconFlow Image Generation</div>
    </a-layout-header>
    <a-layout-content class="app-content">
      <router-view />
    </a-layout-content>
    <a-layout-footer class="app-footer">
      SiliconFlow Image Generation ©2026 Created by Trae AI
    </a-layout-footer>
  </a-layout>
</template>

<script setup lang="ts">
// 根组件，包含基本的布局结构
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
}

.app-header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0 24px;
  display: flex;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
}

.app-logo {
  font-size: 20px;
  font-weight: bold;
  color: #1890ff;
}

.app-content {
  margin: 24px;
  background: #fff;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.app-footer {
  text-align: center;
  background: #f0f2f5;
  padding: 16px;
  color: #666;
}
</style>