<template>
  <div class="image-generation-layout">
    <div class="layout-container">
      <!-- 左侧配置区域 -->
      <div class="left-panel">
        <!-- 页面标题 -->
        <div class="page-title">
          <h2>图片生成配置</h2>
        </div>
        
        <!-- 图片上传 -->
        <ImageUploader />

        <!-- 提示词配置 -->
        <PromptConfig />

        <!-- 模型配置 -->
        <ModelConfig />

        <!-- 参数配置 -->
        <ParamConfig />
      </div>

      <!-- 右侧内容区域 -->
      <div class="right-panel">
        <!-- 生成按钮 -->
        <div class="generate-section">
          <GenerateButton />
        </div>

        <!-- 结果展示 -->
        <div class="result-section">
          <ResultDisplay />
        </div>

        <!-- 日志查看 -->
        <div class="log-section">
          <LogViewer />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { message } from 'ant-design-vue'
import ImageUploader from '@/components/ImageUploader/ImageUploader.vue'
import PromptConfig from '@/components/PromptConfig/PromptConfig.vue'
import ModelConfig from '@/components/ModelConfig/ModelConfig.vue'
import ParamConfig from '@/components/ParamConfig/ParamConfig.vue'
import GenerateButton from '@/components/GenerateButton/GenerateButton.vue'
import ResultDisplay from '@/components/ResultDisplay/ResultDisplay.vue'
import LogViewer from '@/components/LogViewer/LogViewer.vue'
import { useConfigStore } from '@/store/config'

const configStore = useConfigStore()

// 页面初始化时检查后端服务状态
onMounted(async () => {
  try {
    // 调用健康检查接口，获取可用模型列表
    // 注意：这里使用setTimeout模拟API调用，实际项目中应该调用generationApi.healthCheck()
    await new Promise((resolve) => setTimeout(resolve, 1000))
    
    // 模拟健康检查结果
    const mockHealthCheckResponse = {
      status: 'ok',
      availableModels: [
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
      ],
      timestamp: new Date().toISOString()
    }

    // 更新可用模型列表
    configStore.setAvailableModels(mockHealthCheckResponse.availableModels)
    
    message.success('后端服务连接成功')
  } catch (error: any) {
    message.error(`后端服务连接失败：${error.message}`)
  }
})


</script>

<style scoped>
.image-generation-layout {
  min-height: 100vh;
  background: #f0f2f5;
  margin: 0;
  padding: 0;
}

/* 布局容器 */
.layout-container {
  display: flex;
  min-height: 100vh;
}

/* 左侧配置区域 */
.left-panel {
  width: 360px;
  background: #ffffff;
  box-shadow: 2px 0 12px rgba(0, 0, 0, 0.08);
  overflow-y: auto;
  padding: 20px;
  flex-shrink: 0;
}

/* 右侧内容区域 */
.right-panel {
  flex: 1;
  padding: 24px;
  background: #f0f2f5;
  overflow-y: auto;
}

/* 页面标题 */
.page-title {
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.page-title h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

/* 各个内容区块 */
.generate-section,
.result-section,
.log-section {
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 24px;
  overflow: hidden;
}

.result-section,
.log-section {
  padding: 20px;
}

/* 左侧组件间距 */
.left-panel > :deep(.ant-card) {
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* 自定义滚动条 */
.left-panel::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.left-panel::-webkit-scrollbar-track {
  background: #f5f5f5;
}

.left-panel::-webkit-scrollbar-thumb {
  background: #d9d9d9;
  border-radius: 4px;
  transition: background 0.2s ease;
}

.left-panel::-webkit-scrollbar-thumb:hover {
  background: #bfbfbf;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .layout-container {
    flex-direction: column;
  }
  
  .left-panel {
    width: 100%;
    max-height: 50vh;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  }
  
  .right-panel {
    padding: 16px;
  }
  
  .generate-section,
  .result-section,
  .log-section {
    margin-bottom: 16px;
  }
  
  .result-section,
  .log-section {
    padding: 16px;
  }
}
</style>