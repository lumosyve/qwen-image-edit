import { defineStore } from 'pinia'
import type { GenerationParams, Model } from '@/types/api'

export const useConfigStore = defineStore('config', {
  state: () => ({
    apiBaseUrl: import.meta.env?.VITE_API_BASE_URL || '/api',
    availableModels: [] as Model[],
    defaultParams: {
      width: 512,
      height: 512,
      batchSize: 1,
      numInferenceSteps: 50,
      guidanceScale: 7.5,
      seed: null,
    } as GenerationParams,
    maxImageSize: 10, // MB
    supportedImageFormats: ['png', 'jpg', 'jpeg'],
  }),
  actions: {
    setAvailableModels(models: Model[]) {
      this.availableModels = models
    },
    setDefaultParams(params: Partial<GenerationParams>) {
      this.defaultParams = { ...this.defaultParams, ...params }
    },
  },
})