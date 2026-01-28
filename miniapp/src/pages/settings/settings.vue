<template>
  <view class="container">
    <view class="header">
      <text class="title">设置</text>
    </view>
    
    <view class="settings-section">
      <view class="section-title">API配置</view>
      <view class="input-group">
        <text class="label">SiliconFlow API Key</text>
        <input 
          v-model="apiKey" 
          class="api-key-input" 
          placeholder="请输入您的API Key"
          password
        />
        <text class="hint">请在 SiliconFlow 平台获取API Key</text>
      </view>
      
      <button class="save-btn" @tap="saveApiKey">保存</button>
    </view>
    
    <view class="settings-section">
      <view class="section-title">关于</view>
      <view class="about-content">
        <text class="about-text">AI图片编辑器 v1.0.0</text>
        <text class="about-text">基于Qwen/Qwen-Image-Edit-2509模型</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const apiKey = ref('')

// 页面加载时获取已保存的API Key
onMounted(() => {
  const savedApiKey = uni.getStorageSync('siliconFlowApiKey')
  if (savedApiKey) {
    apiKey.value = savedApiKey
  }
})

// 保存API Key
const saveApiKey = () => {
  if (!apiKey.value.trim()) {
    uni.showToast({
      title: '请输入API Key',
      icon: 'none'
    })
    return
  }
  
  try {
    uni.setStorageSync('siliconFlowApiKey', apiKey.value)
    uni.showToast({
      title: '保存成功',
      icon: 'success'
    })
  } catch (error) {
    uni.showToast({
      title: '保存失败',
      icon: 'none'
    })
  }
}
</script>

<style scoped>
.container {
  padding: 20rpx;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.header {
  text-align: center;
  padding: 20rpx 0;
  margin-bottom: 30rpx;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.settings-section {
  background-color: #fff;
  padding: 30rpx;
  border-radius: 10rpx;
  margin-bottom: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.input-group {
  margin-bottom: 30rpx;
}

.label {
  display: block;
  margin-bottom: 15rpx;
  font-size: 28rpx;
  color: #333;
}

.api-key-input {
  width: 100%;
  padding: 20rpx;
  border: 1rpx solid #e0e0e0;
  border-radius: 10rpx;
  font-size: 28rpx;
  box-sizing: border-box;
}

.hint {
  display: block;
  margin-top: 10rpx;
  font-size: 24rpx;
  color: #999;
}

.save-btn {
  width: 100%;
  height: 80rpx;
  background-color: #007AFF;
  color: #fff;
  font-size: 32rpx;
  border-radius: 10rpx;
}

.about-content {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.about-text {
  font-size: 28rpx;
  color: #666;
}
</style>