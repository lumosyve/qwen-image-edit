<template>
  <a-card title="参数配置" :bordered="false" class="param-card">
    <a-form layout="vertical" :model="paramForm">
      <a-row :gutter="[16, 16]">
        <!-- 图片宽度 -->
        <a-col :xs="24" :sm="12" :md="8">
          <a-form-item label="宽度" required>
            <a-input-number
              v-model:value="paramForm.width"
              :min="256"
              :max="2048"
              :step="64"
              placeholder="请输入图片宽度"
              @change="handleParamChange('width')"
            />
            <div class="form-hint">建议值：512-1024</div>
          </a-form-item>
        </a-col>

        <!-- 图片高度 -->
        <a-col :xs="24" :sm="12" :md="8">
          <a-form-item label="高度" required>
            <a-input-number
              v-model:value="paramForm.height"
              :min="256"
              :max="2048"
              :step="64"
              placeholder="请输入图片高度"
              @change="handleParamChange('height')"
            />
            <div class="form-hint">建议值：512-1024</div>
          </a-form-item>
        </a-col>

        <!-- 批量大小 -->
        <a-col :xs="24" :sm="12" :md="8">
          <a-form-item label="批量大小" required>
            <a-input-number
              v-model:value="paramForm.batchSize"
              :min="1"
              :max="8"
              :step="1"
              placeholder="请输入批量大小"
              @change="handleParamChange('batchSize')"
            />
            <div class="form-hint">一次生成的图片数量</div>
          </a-form-item>
        </a-col>

        <!-- 推理步数 -->
        <a-col :xs="24" :sm="12" :md="8">
          <a-form-item label="推理步数" required>
            <a-input-number
              v-model:value="paramForm.numInferenceSteps"
              :min="10"
              :max="200"
              :step="10"
              placeholder="请输入推理步数"
              @change="handleParamChange('numInferenceSteps')"
            />
            <div class="form-hint">步数越多，细节越丰富，但生成速度越慢</div>
          </a-form-item>
        </a-col>

        <!-- 引导比例 -->
        <a-col :xs="24" :sm="12" :md="8">
          <a-form-item label="引导比例" required>
            <a-input-number
              v-model:value="paramForm.guidanceScale"
              :min="1"
              :max="20"
              :step="0.5"
              placeholder="请输入引导比例"
              @change="handleParamChange('guidanceScale')"
            />
            <div class="form-hint">值越大，越遵循提示词，但可能导致图片失真</div>
          </a-form-item>
        </a-col>

        <!-- 随机种子 -->
        <a-col :xs="24" :sm="12" :md="8">
          <a-form-item label="随机种子">
            <a-input-number
              v-model:value="paramForm.seed"
              :min="0"
              :max="999999999"
              :step="1"
              placeholder="请输入随机种子，留空则随机生成"
              @change="handleParamChange('seed')"
            />
            <div class="form-hint">使用相同种子可生成相似图片</div>
          </a-form-item>
        </a-col>
      </a-row>

      <!-- 参数预设模板 -->
      <a-form-item label="参数预设模板">
        <a-space wrap>
          <a-button
            v-for="preset in paramPresets"
            :key="preset.key"
            type="primary"
            size="small"
            @click="applyParamPreset(preset)"
          >
            {{ preset.label }}
          </a-button>
        </a-space>
      </a-form-item>
    </a-form>
  </a-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { useGenerationStore } from '@/store/generation'
import type { GenerationParams } from '@/types/api'

const generationStore = useGenerationStore()

// 表单数据
const paramForm = ref<GenerationParams>({
  width: 512,
  height: 512,
  batchSize: 1,
  numInferenceSteps: 50,
  guidanceScale: 7.5,
  seed: null,
})

// 参数预设模板
const paramPresets = [
  {
    key: 'default',
    label: '默认设置',
    params: {
      width: 512,
      height: 512,
      batchSize: 1,
      numInferenceSteps: 50,
      guidanceScale: 7.5,
      seed: null,
    } as GenerationParams
  },
  {
    key: 'fast',
    label: '快速生成',
    params: {
      width: 512,
      height: 512,
      batchSize: 1,
      numInferenceSteps: 20,
      guidanceScale: 7.5,
      seed: null,
    } as GenerationParams
  },
  {
    key: 'high-quality',
    label: '高质量',
    params: {
      width: 1024,
      height: 1024,
      batchSize: 1,
      numInferenceSteps: 100,
      guidanceScale: 8.0,
      seed: null,
    } as GenerationParams
  },
  {
    key: 'batch-generate',
    label: '批量生成',
    params: {
      width: 512,
      height: 512,
      batchSize: 4,
      numInferenceSteps: 30,
      guidanceScale: 7.0,
      seed: null,
    } as GenerationParams
  }
]

// 组件挂载时，从store获取初始值
onMounted(() => {
  const storeParams = generationStore.generationParams
  paramForm.value = {
    ...paramForm.value,
    ...storeParams
  }
})

// 处理参数变化
const handleParamChange = (paramName: keyof GenerationParams) => {
  generationStore.setGenerationParams({
    [paramName]: paramForm.value[paramName]
  })
}

// 应用参数预设模板
const applyParamPreset = (preset: typeof paramPresets[0]) => {
  paramForm.value = { ...preset.params }
  generationStore.setGenerationParams(preset.params)
  message.success(`已应用${preset.label}预设`)
}
</script>

<style scoped>
.param-card {
  /* 间距由父组件统一控制 */
}

.form-hint {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
}
</style>