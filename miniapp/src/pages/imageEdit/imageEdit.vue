<template>
  <view class="container">
    <view class="header">
      <text class="title">AI图片编辑器</text>
      <text class="settings-link" @tap="goToSettings">设置</text>
    </view>
    
    <!-- 图片上传区域 -->
    <view class="upload-section">
      <view class="section-title">上传图片 (1-3张)</view>
      <ImagePreview 
        :images="images.filter(img => img.url)" 
        :max-count="3"
        @add="selectImage"
        @delete="deleteImage"
        @preview="previewImage"
      />
    </view>
    
    <!-- Prompt输入区域 -->
    <view class="prompt-section">
      <view class="section-title">编辑指令</view>
      <textarea 
        v-model="prompt" 
        class="prompt-input" 
        placeholder="请输入图片编辑指令，例如：将照片转换为油画风格"
      />
      
      <!-- 示例Prompt -->
      <view class="example-prompts">
        <view class="section-title">示例指令</view>
        <scroll-view class="prompt-categories" scroll-x>
          <view 
            v-for="(category, categoryIndex) in promptCategories" 
            :key="categoryIndex"
            class="category-item"
            :class="{ active: selectedCategory === categoryIndex }"
            @tap="selectCategory(categoryIndex)"
          >
            <text>{{ category.name }}</text>
          </view>
        </scroll-view>
        
        <view class="prompt-list">
          <view 
            v-for="(promptItem, promptIndex) in promptCategories[selectedCategory].prompts" 
            :key="promptIndex"
            class="prompt-item"
            @tap="selectPrompt(promptItem)"
          >
            <text>{{ promptItem }}</text>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 参数配置区域 -->
    <view class="config-section">
      <view class="section-title">参数配置</view>
      <view class="config-item">
        <text class="config-label">CFG值: {{ cfg }}</text>
        <slider 
          min="0.1" 
          max="20" 
          step="0.1" 
          :value="cfg" 
          @change="onCfgChange" 
          activeColor="#007AFF"
        />
      </view>
      
      <view class="config-item">
        <text class="config-label">推理步数: {{ numInferenceSteps }}</text>
        <slider 
          min="1" 
          max="100" 
          :value="numInferenceSteps" 
          @change="onStepsChange" 
          activeColor="#007AFF"
        />
      </view>
      
      <view class="config-item">
        <text class="config-label">随机种子: {{ seed }}</text>
        <input 
          type="number" 
          v-model="seed" 
          class="seed-input"
          placeholder="请输入随机种子"
        />
      </view>
    </view>
    
    <!-- 生成按钮 -->
    <button 
      class="generate-btn" 
      @tap="generateImage"
      :disabled="isGenerating"
    >
      {{ isGenerating ? '生成中...' : '生成图片' }}
    </button>
    
    <!-- 结果展示区域 -->
    <view v-if="resultImages.length > 0" class="result-section">
      <view class="section-title">生成结果</view>
      <view class="result-grid">
        <view 
          v-for="(result, index) in resultImages" 
          :key="index"
          class="result-item"
          @tap="previewResultImage(index)"
        >
          <image 
            :src="result.url" 
            class="result-image"
            mode="aspectFill"
          />
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import ImagePreview from '@/components/ImagePreview.vue'
import { editImage, convertImageToBase64 } from '@/utils/api.js'

// 图片上传相关
const images = reactive([
  { url: '', file: null as File | null },
  { url: '', file: null as File | null },
  { url: '', file: null as File | null }
])

// 选择图片
const selectImage = () => {
  // 检查是否已达到最大图片数量
  const uploadedImages = images.filter(img => img.url)
  if (uploadedImages.length >= 3) {
    uni.showToast({
      title: '最多只能上传3张图片',
      icon: 'none'
    })
    return
  }
  
  // 调用uni.chooseImage选择图片
  uni.chooseImage({
    count: 3 - uploadedImages.length, // 还能上传的图片数量
    sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
    sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
    success: function (res) {
      // 将选择的图片添加到images数组中
      res.tempFilePaths.forEach((filePath, index) => {
        // 找到第一个空位插入图片
        const emptyIndex = images.findIndex(img => !img.url)
        if (emptyIndex !== -1) {
          images[emptyIndex].url = filePath
          images[emptyIndex].file = res.tempFiles[index]
        }
      })
    },
    fail: function (err) {
      console.error('选择图片失败', err)
      uni.showToast({
        title: '选择图片失败',
        icon: 'none'
      })
    }
  })
}

// 删除图片
const deleteImage = (index: number) => {
  // 由于我们传递给ImagePreview的是过滤后的数组，需要找到原始数组中的对应项
  const uploadedImages = images.filter(img => img.url)
  if (index >= 0 && index < uploadedImages.length) {
    const originalIndex = images.findIndex(img => img.url === uploadedImages[index].url)
    if (originalIndex !== -1) {
      images[originalIndex].url = ''
      images[originalIndex].file = null
    }
  }
}

// Prompt相关
const prompt = ref('')

// 参数配置
const cfg = ref(7.0)
const numInferenceSteps = ref(20)
const seed = ref(0)

// 状态控制
const isGenerating = ref(false)

// 结果图片
const resultImages = ref<{url: string}[]>([])

// 示例Prompt分类
const promptCategories = ref([
  {
    name: '人像模式',
    prompts: [
      '增强人像的皮肤质感和细节',
      '将人像转换为专业摄影风格',
      '为人像添加柔美的磨皮效果',
      '改善人像的光线和阴影平衡',
      '将人像背景虚化，突出主体',
      '为人像添加自然的美妆效果'
    ]
  },
  {
    name: '处理模式',
    prompts: [
      '提升照片的清晰度和细节',
      '改善照片的光线和色彩平衡',
      '修复老照片的划痕和褪色',
      '去除照片中的噪点和颗粒感',
      '调整照片的对比度和饱和度',
      '校正照片的色偏问题'
    ]
  },
  {
    name: '电影模式',
    prompts: [
      '为照片添加电影级调色效果',
      '将照片转换为复古胶片风格',
      '为照片添加赛博朋克霓虹效果',
      '将照片转换为黑白电影质感',
      '为照片添加史诗级电影氛围',
      '将照片转换为动漫电影风格'
    ]
  },
  {
    name: '风景模式',
    prompts: [
      '将普通风景照转换为明信片风格',
      '增强风景照的色彩饱和度',
      '为风景照添加梦幻光晕效果',
      '将白天风景转换为夜景效果',
      '为风景照添加季节变化效果',
      '增强风景照的景深效果'
    ]
  },
  {
    name: '创意模式',
    prompts: [
      '将照片转换为油画艺术风格',
      '将照片转换为水彩画效果',
      '将照片转换为素描线条风格',
      '为照片添加抽象艺术元素',
      '将照片转换为像素艺术风格',
      '为照片添加科幻未来感'
    ]
  }
])

const selectedCategory = ref(0)

// 选择分类
const selectCategory = (index: number) => {
  selectedCategory.value = index
}

// 选择示例Prompt
const selectPrompt = (promptText: string) => {
  prompt.value = promptText
}

// CFG值变化
const onCfgChange = (e: any) => {
  cfg.value = e.detail.value
}

// 推理步数变化
const onStepsChange = (e: any) => {
  numInferenceSteps.value = e.detail.value
}

// 生成图片
const generateImage = async () => {
  if (!prompt.value.trim()) {
    uni.showToast({
      title: '请输入编辑指令',
      icon: 'none'
    })
    return
  }
  
  // 检查是否有上传图片
  const uploadedImages = images.filter(img => img.url)
  if (uploadedImages.length === 0) {
    uni.showToast({
      title: '请至少上传一张图片',
      icon: 'none'
    })
    return
  }
  
  isGenerating.value = true
  
  try {
    // 转换图片为base64格式
    const base64Images = []
    for (let i = 0; i < uploadedImages.length; i++) {
      // 检查图片是否已经是base64格式
      if (uploadedImages[i].url.startsWith('data:image')) {
        base64Images.push(uploadedImages[i].url)
      } else {
        // 转换本地图片为base64
        const base64Image = await convertImageToBase64(uploadedImages[i].url)
        base64Images.push(base64Image)
      }
    }
    
    // 准备API参数
    const apiParams: any = {
      prompt: prompt.value,
      image: base64Images[0],
      cfg: cfg.value,
      numInferenceSteps: numInferenceSteps.value,
      seed: seed.value || Math.floor(Math.random() * 1000000000)
    }
    
    // 添加额外的图片（如果有）
    if (base64Images.length > 1) {
      apiParams.image2 = base64Images[1]
    }
    if (base64Images.length > 2) {
      apiParams.image3 = base64Images[2]
    }
    
    // 调用API
    const result = await editImage(apiParams)
    
    // 处理结果
    resultImages.value = result.images.map((img: any) => ({
      url: img.url
    }))
    
    isGenerating.value = false
    
    uni.showToast({
      title: '图片生成成功',
      icon: 'success'
    })
  } catch (error: any) {
    isGenerating.value = false
    
    uni.showToast({
      title: error.message || '图片生成失败',
      icon: 'none'
    })
  }
}

// 预览上传的图片
const previewImage = (index: number) => {
  // 由于我们传递给ImagePreview的是过滤后的数组，需要找到原始数组中的对应项
  const uploadedImages = images.filter(img => img.url)
  if (index >= 0 && index < uploadedImages.length) {
    uni.previewImage({
      urls: [uploadedImages[index].url]
    })
  }
}

// 预览结果图片
const previewResultImage = (index: number) => {
  if (index >= 0 && index < resultImages.value.length) {
    uni.previewImage({
      urls: [resultImages.value[index].url]
    })
  }
}

// 跳转到设置页面
const goToSettings = () => {
  uni.navigateTo({
    url: '/pages/settings/settings'
  })
}
</script>

<style scoped>
.container {
  padding: 20rpx;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 30rpx;
  margin-bottom: 30rpx;
  background-color: #fff;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.settings-link {
  font-size: 28rpx;
  color: #007AFF;
  padding: 10rpx 20rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

/* 图片上传区域样式 */
.upload-section {
  background-color: #fff;
  padding: 30rpx;
  border-radius: 10rpx;
  margin-bottom: 30rpx;
}

.image-upload-area {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
}

.image-preview {
  width: 200rpx;
  height: 200rpx;
  border-radius: 10rpx;
  overflow: hidden;
  background-color: #f0f0f0;
  position: relative;
}

.uploaded-image {
  width: 100%;
  height: 100%;
}

.upload-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  background-color: #f8f8f8;
}

.upload-text {
  color: #999;
  font-size: 24rpx;
  text-align: center;
}

.add-image {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f8f8;
}

.add-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.add-text {
  font-size: 60rpx;
  color: #999;
  font-weight: bold;
}

/* Prompt输入区域样式 */
.prompt-section {
  background-color: #fff;
  padding: 30rpx;
  border-radius: 10rpx;
  margin-bottom: 30rpx;
}

.prompt-input {
  width: 100%;
  height: 150rpx;
  padding: 20rpx;
  border: 1rpx solid #e0e0e0;
  border-radius: 10rpx;
  font-size: 28rpx;
  box-sizing: border-box;
  margin-bottom: 30rpx;
}

/* 示例Prompt样式 */
.example-prompts {
  margin-top: 30rpx;
}

.prompt-categories {
  display: flex;
  margin-bottom: 20rpx;
  white-space: nowrap;
}

.category-item {
  padding: 15rpx 30rpx;
  background-color: #f0f0f0;
  border-radius: 30rpx;
  margin-right: 20rpx;
  font-size: 24rpx;
}

.category-item.active {
  background-color: #007AFF;
  color: #fff;
}

.prompt-list {
  display: flex;
  flex-direction: column;
  gap: 15rpx;
}

.prompt-item {
  padding: 20rpx;
  background-color: #f8f8f8;
  border-radius: 10rpx;
  font-size: 26rpx;
  color: #666;
}

/* 参数配置区域样式 */
.config-section {
  background-color: #fff;
  padding: 30rpx;
  border-radius: 10rpx;
  margin-bottom: 30rpx;
}

.config-item {
  margin-bottom: 30rpx;
}

.config-label {
  display: block;
  margin-bottom: 15rpx;
  font-size: 28rpx;
  color: #333;
}

.seed-input {
  width: 100%;
  padding: 15rpx;
  border: 1rpx solid #e0e0e0;
  border-radius: 10rpx;
  font-size: 28rpx;
  box-sizing: border-box;
}

/* 生成按钮样式 */
.generate-btn {
  width: 100%;
  height: 80rpx;
  background-color: #007AFF;
  color: #fff;
  font-size: 32rpx;
  border-radius: 10rpx;
  margin-bottom: 30rpx;
}

.generate-btn[disabled] {
  background-color: #ccc;
}

/* 结果展示区域样式 */
.result-section {
  background-color: #fff;
  padding: 30rpx;
  border-radius: 10rpx;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20rpx;
}

.result-item {
  border-radius: 10rpx;
  overflow: hidden;
}

.result-image {
  width: 100%;
  height: 300rpx;
}
</style>