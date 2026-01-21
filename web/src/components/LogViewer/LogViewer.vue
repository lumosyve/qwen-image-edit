<template>
  <a-card 
    title="日志查看" 
    :bordered="false" 
    class="log-card"
  >
    <template #extra>
      <a-space size="small">
        <!-- 日志级别过滤 -->
        <a-select
          v-model:value="selectedLogLevel"
          placeholder="日志级别"
          style="width: 120px"
          size="small"
          @change="handleLogLevelChange"
        >
          <a-select-option value="info">全部</a-select-option>
          <a-select-option value="warning">警告</a-select-option>
          <a-select-option value="error">错误</a-select-option>
        </a-select>

        <!-- 清空日志按钮 -->
        <a-button
          type="text"
          danger
          size="small"
          icon="clear"
          @click="clearLogs"
          :disabled="filteredLogs.length === 0"
        >
          清空日志
        </a-button>
      </a-space>
    </template>

    <!-- 日志列表 -->
    <div class="log-container">
      <!-- 日志为空时的提示 -->
      <div v-if="filteredLogs.length === 0" class="empty-logs">
        <a-empty
          description="暂无日志信息"
          image="https://gw.alipayobjects.com/zos/antfincdn/ZHrcdLPrvN/empty.svg"
        />
      </div>

      <!-- 日志条目列表 -->
      <a-list
        v-else
        :data-source="filteredLogs"
        class="log-list"
      >
        <template #renderItem="{ item }">
          <a-list-item
            class="log-item"
            :class="`log-level-${item.level}`"
          >
            <a-list-item-meta>
              <template #title>
                <div class="log-header">
                  <span class="log-time">{{ formatTimestamp(item.timestamp) }}</span>
                  <a-tag :color="getLogLevelColor(item.level)" style="margin-left: 8px">
                    {{ item.level.toUpperCase() }}
                  </a-tag>
                </div>
              </template>
              <template #description>
                <div>
                  <p class="log-message">{{ item.message }}</p>
                  <a-collapse
                    v-if="item.details"
                    v-model:activeKey="expandedLogIds"
                    size="small"
                  >
                    <a-collapse-panel :key="item.id" header="查看详情">
                      <pre class="log-details">{{ JSON.stringify(item.details, null, 2) }}</pre>
                    </a-collapse-panel>
                  </a-collapse>
                </div>
              </template>
            </a-list-item-meta>
          </a-list-item>
        </template>
        <template #pagination>
          <a-pagination
            :page-size="10"
            :total="filteredLogs.length"
            show-size-changer
            :show-total="(total: number) => `共 ${total} 条日志`"
          />
        </template>
      </a-list>
    </div>
  </a-card>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { message } from 'ant-design-vue'
import { useLogStore } from '@/store/log'
import type { LogEntry } from '@/types/components'

const logStore = useLogStore()

// 日志级别过滤
const selectedLogLevel = ref('info')

// 日志展开状态
const expandedLogIds = ref<string[]>([])

// 计算属性：过滤后的日志
const filteredLogs = computed(() => {
  return logStore.filteredLogs
})

// 处理日志级别变化
const handleLogLevelChange = (level: string) => {
  logStore.setLogLevel(level as 'info' | 'warning' | 'error')
}

// 格式化时间戳
const formatTimestamp = (timestamp: string): string => {
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  })
}

// 获取日志级别颜色
const getLogLevelColor = (level: LogEntry['level']): string => {
  switch (level) {
    case 'info':
      return 'blue'
    case 'warning':
      return 'orange'
    case 'error':
      return 'red'
    default:
      return 'default'
  }
}

// 清空日志
const clearLogs = () => {
  logStore.clearLogs()
  expandedLogIds.value = []
  message.success('日志已清空')
}
</script>

<style scoped>
.log-card {
  margin-bottom: 16px;
}

.log-container {
  max-height: 400px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.empty-logs {
  padding: 40px 0;
  text-align: center;
}

.log-list {
  flex: 1;
  overflow-y: auto;
  max-height: 350px;
}

.log-item {
  border-bottom: 1px solid #f0f0f0;
  padding: 12px 0;
  transition: background-color 0.3s;
}

.log-item:hover {
  background-color: #fafafa;
}

.log-header {
  display: flex;
  align-items: center;
  font-size: 12px;
  margin-bottom: 4px;
}

.log-time {
  color: #999;
  font-family: monospace;
}

.log-message {
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
  word-break: break-all;
}

.log-details {
  margin: 8px 0 0 0;
  padding: 12px;
  background: #f5f5f5;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 12px;
  line-height: 1.5;
  white-space: pre-wrap;
}

/* 日志级别样式 */
.log-level-info .log-message {
  color: #1890ff;
}

.log-level-warning .log-message {
  color: #faad14;
}

.log-level-error .log-message {
  color: #f5222d;
}

/* 滚动条样式 */
.log-list::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.log-list::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.log-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.log-list::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

@media (max-width: 768px) {
  .log-container {
    max-height: 300px;
  }

  .log-list {
    max-height: 250px;
  }
}
</style>