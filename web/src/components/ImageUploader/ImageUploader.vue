<template>
  <a-card title="图片上传" :bordered="false" class="uploader-card">
    <a-upload
      v-model:file-list="fileList"
      :multiple="true"
      list-type="picture-card"
      :before-upload="beforeUpload"
      :custom-request="customRequest"
      :on-remove="handleRemove"
      :on-preview="handlePreview"
    >
      <div v-if="fileList.length < 5">
        <span class="upload-icon">
          <UploadOutlined />
        </span>
        <div class="upload-text">上传图片</div>
        <div class="upload-hint">支持 PNG、JPG、JPEG 格式，单张不超过 10MB</div>
      </div>
    </a-upload>
    <a-modal
      v-model:open="previewVisible"
      title="图片预览"
      footer="null"
      width="800px"
    >
      <img :src="previewImage" alt="预览" style="width: 100%" />
    </a-modal>
  </a-card>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { UploadOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import type { UploadProps, UploadFile } from 'ant-design-vue'
import { useGenerationStore } from '@/store/generation'
import { useConfigStore } from '@/store/config'

const generationStore = useGenerationStore()
const configStore = useConfigStore()

// 文件列表
const fileList = ref<UploadFile[]>([])
// 预览相关
const previewVisible = ref(false)
const previewImage = ref('')

// 监听文件列表变化，更新store
watch(fileList, (newList) => {
  generationStore.setInputImages(newList)
}, { deep: true })

// 上传前验证
const beforeUpload: UploadProps['beforeUpload'] = (file) => {
  // 验证文件类型
  const isImage = configStore.supportedImageFormats.includes(file.type.split('/')[1])
  if (!isImage) {
    message.error(`只支持 ${configStore.supportedImageFormats.join(', ')} 格式的图片`)
    return false
  }
  
  // 验证文件大小
  const isLt10M = file.size / 1024 / 1024 < configStore.maxImageSize
  if (!isLt10M) {
    message.error(`图片大小不能超过 ${configStore.maxImageSize}MB`)
    return false
  }
  
  return true
}

// 自定义上传逻辑（实际上只是预览，不发送请求）
const customRequest: UploadProps['customRequest'] = (options) => {
  // 模拟上传成功
  setTimeout(() => {
    options.onSuccess?.({})
  }, 500)
}

// 移除文件
const handleRemove: UploadProps['onRemove'] = (file) => {
  const index = fileList.value.findIndex((item) => item.uid === file.uid)
  if (index !== -1) {
    fileList.value.splice(index, 1)
  }
  message.success('图片已移除')
}

// 预览文件
const handlePreview: UploadProps['onPreview'] = (file) => {
  previewImage.value = file.url || (file.thumbUrl as string)
  previewVisible.value = true
}
</script>

<style scoped>
.uploader-card {
  /* 间距由父组件统一控制 */
}

.upload-icon {
  font-size: 24px;
  color: #1890ff;
  display: block;
  margin-bottom: 8px;
}

.upload-text {
  font-size: 16px;
  margin-bottom: 4px;
}

.upload-hint {
  font-size: 12px;
  color: #666;
}
</style>