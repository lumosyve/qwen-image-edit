import { createRouter, createWebHistory } from 'vue-router'
import ImageGenerationView from '@/views/ImageGenerationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env?.BASE_URL || ''),
  routes: [
    {
      path: '/',
      name: 'image-generation',
      component: ImageGenerationView,
      meta: {
        title: 'SiliconFlow图片生成',
      },
    },
    // 可以添加更多路由
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
  ],
})

// 路由守卫：设置页面标题
router.beforeEach((to, _from, next) => {
  if (to.meta.title) {
    document.title = `${to.meta.title as string} - SiliconFlow图片生成`
  } else {
    document.title = 'SiliconFlow图片生成'
  }
  next()
})

export default router