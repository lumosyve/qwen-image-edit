<template>
  <a-card title="模型配置" :bordered="false" class="model-card">
    <a-form layout="vertical" :model="modelForm">
      <!-- 模型选择 -->
      <a-form-item label="选择模型" required>
        <a-select
          v-model:value="modelForm.selectedModel"
          placeholder="请选择要使用的模型"
          style="width: 100%"
          @change="handleModelChange"
        >
          <a-select-option
            v-for="model in availableModels"
            :key="model.id"
            :value="model.id"
          >
            {{ model.name }}
          </a-select-option>
        </a-select>
      </a-form-item>

      <!-- 模型描述 -->
      <a-card 
        v-if="selectedModelDetail" 
        size="small"
        :title="selectedModelDetail.name"
        class="model-detail-card"
      >
        <p>{{ selectedModelDetail.description }}</p>
        <div class="model-params">
          <strong>支持参数：</strong>
          <a-tag 
            v-for="param in selectedModelDetail.supportedParams" 
            :key="param" 
            color="green" 
            size="small"
            style="margin: 4px 4px 0 0"
          >
            {{ param }}
          </a-tag>
        </div>
      </a-card>
    </a-form>
  </a-card>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { useGenerationStore } from '@/store/generation'
import { useConfigStore } from '@/store/config'
import type { Model } from '@/types/api'

const generationStore = useGenerationStore()
const configStore = useConfigStore()

// 表单数据
const modelForm = ref({
  selectedModel: '',
})

// 可用模型列表
const availableModels = ref<Model[]>([
  // 模拟数据，实际会从API获取
  {
    id: 'model-1',
    name: 'SiliconFlow-v1',
    description: '通用图片生成模型，适合大多数场景',
    supportedParams: ['width', 'height', 'batchSize', 'numInferenceSteps', 'guidanceScale', 'seed'],
    defaultParams: {
      width: 512,
      height: 512,
      batchSize: 1,
      numInferenceSteps: 50,
      guidanceScale: 7.5,
      seed: null
    }
  },
  {
    id: 'model-2',
    name: 'SiliconFlow-v2',
    description: '高清图片生成模型，适合需要高分辨率的场景',
    supportedParams: ['width', 'height', 'batchSize', 'numInferenceSteps', 'guidanceScale', 'seed'],
    defaultParams: {
      width: 1024,
      height: 1024,
      batchSize: 1,
      numInferenceSteps: 100,
      guidanceScale: 8.0,
      seed: null
    }
  },
  {
    id: 'model-3',
    name: 'SiliconFlow-anime',
    description: '动漫风格图片生成模型，适合生成动漫角色和场景',
    supportedParams: ['width', 'height', 'batchSize', 'numInferenceSteps', 'guidanceScale', 'seed'],
    defaultParams: {
      width: 768,
      height: 1024,
      batchSize: 1,
      numInferenceSteps: 50,
      guidanceScale: 7.0,
      seed: null
    }
  }
])

// 计算属性：当前选中的模型详情
const selectedModelDetail = computed(() => {
  if (!modelForm.value.selectedModel) return null
  return availableModels.value.find(model => model.id === modelForm.value.selectedModel)
})

// 组件挂载时，从store获取初始值
onMounted(() => {
  modelForm.value.selectedModel = generationStore.selectedModel
  
  // 模拟从API获取可用模型
  // 实际项目中应该调用generationApi.healthCheck()获取
  configStore.setAvailableModels(availableModels.value)
})

// 监听模型选择变化，更新store并应用默认参数
const handleModelChange = () => {
  const modelId = modelForm.value.selectedModel
  generationStore.setSelectedModel(modelId)
  
  const modelDetail = selectedModelDetail.value
  if (modelDetail) {
    // 应用模型默认参数
    generationStore.setGenerationParams(modelDetail.defaultParams)
    message.success(`已选择模型：${modelDetail.name}`)
  }
}
</script>

<style scoped>
.model-card {
  /* 间距由父组件统一控制 */
}

.model-detail-card {
  margin-top: 16px;
}

.model-params {
  margin-top: 8px;
}

:deep(.ant-tag) {
  margin-right: 8px;
  margin-bottom: 8px;
}
</style>