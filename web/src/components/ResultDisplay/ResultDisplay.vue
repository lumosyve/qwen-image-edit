<template>
  <a-card 
    title="生成结果" 
    :bordered="false" 
    class="result-card"
  >
    <template #extra>
      <a-space size="small">
        <!-- 下载全部按钮 -->
        <a-button
          v-if="generatedImages.length > 0"
          type="primary"
          size="small"
          icon="download"
          @click="downloadAllImages"
        >
          下载全部
        </a-button>

        <!-- 清空结果按钮 -->
        <a-button
          v-if="generatedImages.length > 0"
          size="small"
          danger
          icon="delete"
          @click="clearResults"
        >
          清空结果
        </a-button>
      </a-space>
    </template>

    <!-- 生成结果为空时的提示 -->
    <div v-if="generatedImages.length === 0" class="empty-result">
      <a-empty
        description="暂无生成结果"
        image="https://gw.alipayobjects.com/zos/antfincdn/ZHrcdLPrvN/empty.svg"
      >
        <template #extra>
          <a-button type="primary">开始生成</a-button>
        </template>
      </a-empty>
    </div>

    <!-- 生成结果展示 -->
    <div v-else class="result-grid">
      <div 
        v-for="(image, index) in generatedImages" 
        :key="image.id"
        class="result-item"
      >
        <a-card
          hoverable
          class="image-card"
        >
          <div class="image-wrapper">
            <a-image
              :src="image.url"
              :preview="{
                visible: previewImageId === image.id,
                onVisibleChange: (visible: boolean) => {
                  if (!visible) {
                    previewImageId = ''
                  }
                }
              }"
              @click="previewImageId = image.id"
              fit="contain"
            >
              <template #placeholder>
                <div class="image-placeholder">
                  <LoadingOutlined />
                </div>
              </template>
            </a-image>
          </div>

          <!-- 图片信息 -->
          <div class="image-info">
            <p class="image-index">图片 {{ index + 1 }}</p>
            <p class="image-size">{{ image.width }} × {{ image.height }}</p>
            <p class="image-seed">Seed: {{ image.seed }}</p>
          </div>

          <!-- 图片操作 -->
          <div class="image-actions">
            <a-space size="small">
              <a-button
                type="text"
                icon="download"
                @click.stop="downloadImage(image)"
                title="下载图片"
              >
                下载
              </a-button>
              <a-button
                type="text"
                icon="copy"
                @click.stop="copyImageUrl(image)"
                title="复制链接"
              >
                复制链接
              </a-button>
              <a-button
                type="text"
                icon="share-alt"
                @click.stop="shareImage(image)"
                title="分享图片"
              >
                分享
              </a-button>
            </a-space>
          </div>
        </a-card>
      </div>
    </div>
  </a-card>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { LoadingOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import { useGenerationStore } from '@/store/generation'
import type { GeneratedImage } from '@/types/api'

const generationStore = useGenerationStore()



// 预览图片ID
const previewImageId = ref('')

// 计算属性：生成的图片列表
const generatedImages = computed(() => {
  return generationStore.generatedImages
})

// 下载单张图片
const downloadImage = async (image: GeneratedImage) => {
  try {
    const response = await fetch(image.url)
    const blob = await response.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `generated-image-${image.id}.png`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    message.success('图片下载成功')
  } catch (error) {
    message.error('图片下载失败')
    console.error('下载图片失败:', error)
  }
}

// 下载全部图片
const downloadAllImages = () => {
  generatedImages.value.forEach((image, index) => {
    // 使用setTimeout避免浏览器阻塞
    setTimeout(() => {
      downloadImage(image)
    }, index * 500)
  })
  message.success(`开始下载 ${generatedImages.value.length} 张图片`)
}

// 复制图片链接
const copyImageUrl = async (image: GeneratedImage) => {
  try {
    await navigator.clipboard.writeText(image.url)
    message.success('图片链接已复制到剪贴板')
  } catch (error) {
    // 降级方案：使用input元素复制
    const input = document.createElement('input')
    input.value = image.url
    document.body.appendChild(input)
    input.select()
    document.execCommand('copy')
    document.body.removeChild(input)
    message.success('图片链接已复制到剪贴板')
  }
}

// 分享图片
const shareImage = (image: GeneratedImage) => {
  // 检查浏览器是否支持分享API
  if (navigator.share) {
    navigator.share({
      title: '生成的图片',
      text: '查看我生成的图片',
      url: image.url,
    }).catch((error) => {
      console.error('分享失败:', error)
      message.error('分享失败，请重试')
    })
  } else {
    // 不支持分享API时，复制链接
    copyImageUrl(image)
    message.success('图片链接已复制，您可以手动分享')
  }
}

// 清空结果
const clearResults = () => {
  generationStore.setGeneratedImages([])
  message.success('已清空生成结果')
}
</script>

<style scoped>
.result-card {
  margin-bottom: 16px;
}

.empty-result {
  padding: 40px 0;
  text-align: center;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.result-item {
  transition: transform 0.3s ease;
}

.result-item:hover {
  transform: translateY(-4px);
}

.image-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.image-wrapper {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
}

.image-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  font-size: 24px;
  color: #999;
}

.image-info {
  margin: 12px 0;
  font-size: 12px;
  color: #666;
  line-height: 1.5;
}

.image-index {
  font-weight: bold;
  margin-bottom: 4px;
}

.image-size,
.image-seed {
  margin: 2px 0;
}

.image-actions {
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

@media (max-width: 768px) {
  .result-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
  }

  .image-wrapper {
    height: 150px;
  }
}
</style>