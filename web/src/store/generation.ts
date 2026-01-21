import { defineStore } from 'pinia'
import type { UploadFile } from 'ant-design-vue'
import type { GenerationParams, GeneratedImage } from '@/types/api'

export const useGenerationStore = defineStore('generation', {
  state: () => ({
    inputImages: [] as UploadFile[],
    prompt: '',
    negativePrompt: '',
    selectedModel: '',
    generationParams: {
      width: 512,
      height: 512,
      batchSize: 1,
      numInferenceSteps: 50,
      guidanceScale: 7.5,
      seed: null,
    } as GenerationParams,
    generatedImages: [] as GeneratedImage[],
    isGenerating: false,
    generationStatus: 'idle' as 'idle' | 'generating' | 'success' | 'error',
    generationProgress: 0,
    generationTime: 0,
    errorMessage: null as string | null,
  }),
  actions: {
    setInputImages(images: UploadFile[]) {
      this.inputImages = images
    },
    setPrompt(prompt: string) {
      this.prompt = prompt
    },
    setNegativePrompt(negativePrompt: string) {
      this.negativePrompt = negativePrompt
    },
    setSelectedModel(model: string) {
      this.selectedModel = model
    },
    setGenerationParams(params: Partial<GenerationParams>) {
      this.generationParams = { ...this.generationParams, ...params }
    },
    setGeneratedImages(images: GeneratedImage[]) {
      this.generatedImages = images
    },
    setIsGenerating(isGenerating: boolean) {
      this.isGenerating = isGenerating
    },
    setGenerationStatus(status: 'idle' | 'generating' | 'success' | 'error') {
      this.generationStatus = status
    },
    setGenerationProgress(progress: number) {
      this.generationProgress = progress
    },
    setGenerationTime(time: number) {
      this.generationTime = time
    },
    setErrorMessage(message: string | null) {
      this.errorMessage = message
    },
    resetState() {
      this.generatedImages = []
      this.isGenerating = false
      this.generationStatus = 'idle'
      this.generationProgress = 0
      this.generationTime = 0
      this.errorMessage = null
    },
  },
})