<template>
  <a-card 
    title="提示词配置" 
    :bordered="true" 
    class="prompt-card"
    :style="{ border: '1px solid #1890ff', boxShadow: '0 4px 12px rgba(24, 144, 255, 0.15)' }"
  >
    <a-form layout="vertical" :model="promptForm">
      <!-- 正面提示词 -->
      <a-form-item label="手动输入提示词" required :label-col="{ span: 24 }">
        <a-input
          type="textarea"
          v-model:value="promptForm.prompt"
          :auto-size="{ minRows: 4, maxRows: 10 }"
          placeholder="请在此输入您的提示词，描述您想要生成的图片内容..."
          @input="handlePromptChange"
          :style="{ fontSize: '14px' }"
          autofocus
        />
        <div class="form-hint" style="margin-top: 8px; font-weight: 500; color: #1890ff;">💡 提示：您可以直接输入提示词，或点击下方模板追加</div>
      </a-form-item>

      <!-- 负面提示词 -->
      <a-form-item label="手动输入负面提示词" :label-col="{ span: 24 }">
        <a-input
          type="textarea"
          v-model:value="promptForm.negativePrompt"
          :auto-size="{ minRows: 2, maxRows: 6 }"
          placeholder="请在此输入负面提示词，描述您不想要的内容..."
          @input="handleNegativePromptChange"
          :style="{ fontSize: '14px' }"
        />
        <div class="form-hint">负面提示词会指导AI避免生成您不想要的内容</div>
      </a-form-item>

      <!-- 常用提示词模板 -->
      <a-form-item label="快速添加提示词模板" :label-col="{ span: 24 }">
        <div style="margin-bottom: 8px; font-weight: 500; color: #666;">点击以下模板可直接追加到提示词中：</div>
        <a-space wrap>
          <a-tag
            v-for="template in promptTemplates"
            :key="template.key"
            color="blue"
            @click="applyPromptTemplate(template)"
            :style="{ cursor: 'pointer', margin: '4px' }"
          >
            {{ template.label }}
          </a-tag>
        </a-space>
      </a-form-item>
    </a-form>
  </a-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { useGenerationStore } from '@/store/generation'

const generationStore = useGenerationStore()

// 表单数据
const promptForm = ref({
  prompt: '',
  negativePrompt: '',
})

// 常用提示词模板
const promptTemplates = [
  {
    key: 'realistic',
    label: '写实风格',
    prompt: 'photo realistic, high resolution, detailed texture, natural lighting',
    negativePrompt: 'cartoon, anime, sketch, low quality, blurry'
  },
  {
    key: 'anime',
    label: '动漫风格',
    prompt: 'anime style, vibrant colors, detailed line art, character design',
    negativePrompt: 'realistic, photo, blurry, low resolution'
  },
  {
    key: 'fantasy',
    label: '奇幻风格',
    prompt: 'fantasy world, magical, mythical creatures, epic scenery',
    negativePrompt: 'modern, realistic, urban, low quality'
  },
  {
    key: 'cyberpunk',
    label: '赛博朋克',
    prompt: 'cyberpunk city, neon lights, futuristic, high tech, dystopian',
    negativePrompt: 'rural, historical, low tech, blurry'
  }
]

// 组件挂载时，从store获取初始值
onMounted(() => {
  promptForm.value.prompt = generationStore.prompt
  promptForm.value.negativePrompt = generationStore.negativePrompt
})

// 处理提示词变化
const handlePromptChange = () => {
  generationStore.setPrompt(promptForm.value.prompt)
}

// 处理负面提示词变化
const handleNegativePromptChange = () => {
  generationStore.setNegativePrompt(promptForm.value.negativePrompt)
}

// 应用提示词模板
const applyPromptTemplate = (template: typeof promptTemplates[0]) => {
  // 追加正面提示词
  if (promptForm.value.prompt.trim()) {
    // 如果已有内容，添加逗号分隔
    promptForm.value.prompt += `, ${template.prompt}`
  } else {
    // 如果没有内容，直接使用模板
    promptForm.value.prompt = template.prompt
  }
  
  // 追加负面提示词
  if (promptForm.value.negativePrompt.trim()) {
    // 如果已有内容，添加逗号分隔
    promptForm.value.negativePrompt += `, ${template.negativePrompt}`
  } else {
    // 如果没有内容，直接使用模板
    promptForm.value.negativePrompt = template.negativePrompt
  }
  
  // 更新store状态
  generationStore.setPrompt(promptForm.value.prompt)
  generationStore.setNegativePrompt(promptForm.value.negativePrompt)
  
  message.success(`已追加${template.label}模板内容`)
}
</script>

<style scoped>
.prompt-card {
  /* 确保卡片正常显示 */
  width: 100%;
  min-height: 100px;
  display: block;
  visibility: visible;
  opacity: 1;
}

.form-hint {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
}

:deep(.ant-tag) {
  cursor: pointer;
  user-select: none;
}

:deep(.ant-tag:hover) {
  opacity: 0.8;
}
</style>