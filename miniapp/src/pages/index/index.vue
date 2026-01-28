<!--
 * @Author: ZhengJie jabarizheng@gmail.com
 * @Date: 2025-11-03 20:12:44
 * @LastEditors: ZhengJie jabarizheng@gmail.com
 * @LastEditTime: 2026-01-29 02:05:28
 * @FilePath: /miniapp/src/pages/index/index.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <view class="content">
    <image class="logo" src="/static/logo.png" />
    <view class="text-area">
      <text class="title">{{ title }}</text>
    </view>
    <button class="nav-button" @tap="goToImageEdit">前往图片编辑器</button>
    <button class="nav-button" @tap="goToSettings">设置</button>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const title = ref('Hello')

const goToImageEdit = () => {
  uni.navigateTo({
    url: '/pages/imageEdit/imageEdit'
  })
}

const goToSettings = () => {
  uni.navigateTo({
    url: '/pages/settings/settings'
  })
}
</script>

<style>
.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.logo {
  height: 200rpx;
  width: 200rpx;
  margin-top: 200rpx;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 50rpx;
}

.text-area {
  display: flex;
  justify-content: center;
}

.title {
  font-size: 36rpx;
  color: #8f8f94;
}

.nav-button {
  margin-top: 50rpx;
  width: 300rpx;
  height: 80rpx;
  background-color: #007AFF;
  color: #fff;
  font-size: 32rpx;
  border-radius: 10rpx;
}
</style>
