import { defineStore } from 'pinia'
import type { LogEntry } from '@/types/components'

export const useLogStore = defineStore('log', {
  state: () => ({
    logs: [] as LogEntry[],
    logLevel: 'info' as 'info' | 'warning' | 'error',
  }),
  actions: {
    addLog(log: Omit<LogEntry, 'id' | 'timestamp'>) {
      const newLog: LogEntry = {
        id: Date.now().toString(),
        timestamp: new Date().toISOString(),
        ...log,
      }
      this.logs.unshift(newLog)
    },
    clearLogs() {
      this.logs = []
    },
    setLogLevel(level: 'info' | 'warning' | 'error') {
      this.logLevel = level
    },
  },
  getters: {
    filteredLogs: (state) => {
      const levels = { info: 0, warning: 1, error: 2 }
      const currentLevel = levels[state.logLevel]
      return state.logs.filter(log => levels[log.level] >= currentLevel)
    },
  },
})