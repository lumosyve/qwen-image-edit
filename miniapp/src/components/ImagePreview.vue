<template>
  <view class="image-preview-container">
    <view 
      class="image-item"
      v-for="(image, index) in images" 
      :key="index"
      @tap="previewImage(index)"
    >
      <image 
        :src="image.url" 
        class="preview-image"
        mode="aspectFill"
      />
      <view 
        v-if="showDelete" 
        class="delete-btn"
        @tap.stop="deleteImage(index)"
      >
        ×
      </view>
    </view>
    
    <view 
      v-if="showAdd && images.length < maxCount"
      class="add-image-btn"
      @tap="addImage"
    >
      +
    </view>
  </view>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  // 图片数组，每个元素包含url属性
  images: {
    type: Array,
    required: true,
    default: () => []
  },
  // 是否显示删除按钮
  showDelete: {
    type: Boolean,
    default: true
  },
  // 是否显示添加按钮
  showAdd: {
    type: Boolean,
    default: true
  },
  // 最大图片数量
  maxCount: {
    type: Number,
    default: 3
  }
})

const emit = defineEmits(['preview', 'delete', 'add'])

// 预览图片
const previewImage = (index) => {
  emit('preview', index)
}

// 删除图片
const deleteImage = (index) => {
  emit('delete', index)
}

// 添加图片
const addImage = () => {
  emit('add')
}
</script>

<style scoped>
.image-preview-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
}

.image-item {
  position: relative;
  width: 200rpx;
  height: 200rpx;
  border-radius: 10rpx;
  overflow: hidden;
}

.preview-image {
  width: 100%;
  height: 100%;
}

.delete-btn {
  position: absolute;
  top: 10rpx;
  right: 10rpx;
  width: 80rpx;
  height: 80rpx;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 60rpx;
  font-weight: bold;
}

.add-image-btn {
  width: 200rpx;
  height: 200rpx;
  border: 2rpx dashed #ccc;
  border-radius: 10rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 100rpx;
  color: #ccc;
  font-weight: bold;
}
</style>