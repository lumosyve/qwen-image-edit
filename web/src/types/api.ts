import type { UploadFile } from 'ant-design-vue'

export interface GenerationParams {
  width: number
  height: number
  batchSize: number
  numInferenceSteps: number
  guidanceScale: number
  seed: number | null
}

export interface GeneratedImage {
  id: string
  url: string
  base64: string
  width: number
  height: number
  seed: number
}

export interface GenerationRequest {
  images: UploadFile[]
  model: string
  prompt: string
  negativePrompt: string
  width: number
  height: number
  batchSize: number
  numInferenceSteps: number
  guidanceScale: number
  seed?: number
}

export interface GenerationResponse {
  success: boolean
  message: string
  data?: {
    generatedImages: GeneratedImage[]
    seed: number
    generationTime: number
  }
  error?: string
}

export interface Model {
  id: string
  name: string
  description: string
  supportedParams: string[]
  defaultParams: Partial<GenerationParams>
}

export interface HealthCheckResponse {
  status: string
  availableModels: Model[]
  timestamp: string
}