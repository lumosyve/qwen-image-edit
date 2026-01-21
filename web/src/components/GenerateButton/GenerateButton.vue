<template>
  <a-card title="生成设置" :bordered="false" class="generate-card">
    <div class="generate-content">
      <!-- 生成按钮 -->
      <a-space size="large" direction="vertical" style="width: 100%">
        <a-button
          type="primary"
          size="large"
          :loading="generationStore.isGenerating"
          :disabled="!canGenerate"
          @click="handleGenerate"
          block
        >
          <template #icon>
            <FireOutlined />
          </template>
          {{ generateButtonText }}
        </a-button>

        <!-- 生成状态 -->
        <div v-if="generationStore.isGenerating" class="generation-status">
          <a-progress
            :percent="generationStore.generationProgress"
            :status="generationStore.generationStatus === 'error' ? 'exception' : 'active'"
            stroke-linecap="round"
          />
          <div class="status-text">
            {{ statusText }}
            <a-tag
              :color="getStatusColor(generationStore.generationStatus)"
              style="margin-left: 8px"
            >
              {{ generationStore.generationStatus }}
            </a-tag>
          </div>
        </div>

        <!-- 生成结果统计 -->
        <div v-else-if="generationStore.generationStatus === 'success'" class="generation-result">
          <a-alert
            message="生成成功"
            description="已生成 {{ generationStore.generatedImages.length }} 张图片，耗时 {{ (generationStore.generationTime / 1000).toFixed(2) }}s"
            type="success"
            show-icon
          />
        </div>

        <!-- 错误信息 -->
        <div v-else-if="generationStore.errorMessage" class="generation-error">
          <a-alert
            message="生成失败"
            description="{{ generationStore.errorMessage }}"
            type="error"
            show-icon
          />
        </div>

        <!-- 生成前提示 -->
        <div v-else class="generation-tip">
          <a-alert
            message="准备生成"
            description="请确保已上传图片、填写提示词并选择模型"
            type="info"
            show-icon
          />
        </div>
      </a-space>
    </div>
  </a-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { FireOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import { useGenerationStore } from '@/store/generation'

const generationStore = useGenerationStore()

// 计算属性：是否可以生成图片
const canGenerate = computed(() => {
  return (
    generationStore.inputImages.length > 0 &&
    generationStore.prompt.trim() !== '' &&
    generationStore.selectedModel !== ''
  )
})

// 计算属性：生成按钮文本
const generateButtonText = computed(() => {
  if (generationStore.isGenerating) {
    return '生成中...'
  }
  if (generationStore.generationStatus === 'success') {
    return '重新生成'
  }
  return '开始生成'
})

// 计算属性：生成状态文本
const statusText = computed(() => {
  switch (generationStore.generationStatus) {
    case 'idle':
      return '准备生成'
    case 'generating':
      return '正在生成图片...'
    case 'success':
      return '生成成功'
    case 'error':
      return '生成失败'
    default:
      return '未知状态'
  }
})

// 获取状态颜色
const getStatusColor = (status: string): string => {
  switch (status) {
    case 'idle':
      return 'blue'
    case 'generating':
      return 'processing'
    case 'success':
      return 'success'
    case 'error':
      return 'error'
    default:
      return 'default'
  }
}

// 处理生成按钮点击
const handleGenerate = async () => {
  if (!canGenerate.value) {
    message.error('请确保已上传图片、填写提示词并选择模型')
    return
  }

  try {
    // 重置状态
    generationStore.resetState()
    generationStore.setIsGenerating(true)
    generationStore.setGenerationStatus('generating')
    generationStore.setGenerationProgress(0)

    // 模拟生成进度
    const progressInterval = setInterval(() => {
      if (generationStore.generationProgress < 90) {
        generationStore.setGenerationProgress(
          generationStore.generationProgress + Math.random() * 10
        )
      }
    }, 500)

    // 准备请求数据
    const requestData = {
      images: generationStore.inputImages,
      model: generationStore.selectedModel,
      prompt: generationStore.prompt,
      negativePrompt: generationStore.negativePrompt,
      width: generationStore.generationParams.width,
      height: generationStore.generationParams.height,
      batchSize: generationStore.generationParams.batchSize,
      numInferenceSteps: generationStore.generationParams.numInferenceSteps,
      guidanceScale: generationStore.generationParams.guidanceScale,
      seed: generationStore.generationParams.seed,
    }

    // 调用API生成图片
    // 注意：这里使用setTimeout模拟API调用，实际项目中应该调用generationApi.generateImages(requestData)
    const startTime = Date.now()
    await new Promise((resolve) => setTimeout(resolve, 5000)) // 模拟API调用延迟
    
    // 模拟生成结果
    const mockGeneratedImages = Array.from({ length: requestData.batchSize }, (_, index) => ({
      id: `image-${Date.now()}-${index}`,
      url: `https://picsum.photos/seed/${Date.now() + index}/${requestData.width}/${requestData.height}`,
      base64: '',
      width: requestData.width,
      height: requestData.height,
      seed: requestData.seed || Math.floor(Math.random() * 1000000),
    }))

    const endTime = Date.now()
    const generationTime = endTime - startTime

    // 清除进度定时器
    clearInterval(progressInterval)

    // 更新状态
    generationStore.setGenerationProgress(100)
    generationStore.setGeneratedImages(mockGeneratedImages)
    generationStore.setGenerationStatus('success')
    generationStore.setGenerationTime(generationTime)
    generationStore.setIsGenerating(false)

    message.success('图片生成成功')
  } catch (error: any) {
    generationStore.setGenerationStatus('error')
    generationStore.setErrorMessage(error.message || '生成图片失败，请重试')
    generationStore.setIsGenerating(false)
    message.error('图片生成失败')
  }
}
</script>

<style scoped>
.generate-card {
  margin-bottom: 16px;
}

.generate-content {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 16px 0;
}

.generation-status {
  width: 100%;
}

.status-text {
  margin-top: 12px;
  text-align: center;
  font-size: 14px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.generation-result,
.generation-error,
.generation-tip {
  width: 100%;
}
</style>