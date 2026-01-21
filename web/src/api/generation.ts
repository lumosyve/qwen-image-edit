import apiClient from './index'
import type { GenerationRequest, GenerationResponse, HealthCheckResponse } from '@/types/api'

export const generationApi = {
  // 健康检查
  healthCheck: async (): Promise<HealthCheckResponse> => {
    const response = await apiClient.get<HealthCheckResponse>('/health')
    return response.data
  },
  
  // 生成图片
  generateImages: async (request: GenerationRequest): Promise<GenerationResponse> => {
    const formData = new FormData()
    
    // 添加图片文件
    request.images.forEach((image) => {
      formData.append('images', image.originFileObj as File)
    })
    
    // 添加其他参数
    formData.append('model', request.model)
    formData.append('prompt', request.prompt)
    formData.append('negative_prompt', request.negativePrompt)
    formData.append('width', request.width.toString())
    formData.append('height', request.height.toString())
    formData.append('batch_size', request.batchSize.toString())
    formData.append('num_inference_steps', request.numInferenceSteps.toString())
    formData.append('guidance_scale', request.guidanceScale.toString())
    
    if (request.seed) {
      formData.append('seed', request.seed.toString())
    }
    
    const response = await apiClient.post<GenerationResponse>('/generate-images', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
}