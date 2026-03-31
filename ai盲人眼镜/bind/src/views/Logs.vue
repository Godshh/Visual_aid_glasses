<template>
  <div class="logs">
    <!-- Top stats + controls -->
    <div class="logs-top-box">
      <div class="top-row">
        <h1 class="page-title">语音交互日志</h1>
        <div class="top-actions">
          <button class="btn btn-secondary" @click="exportLogs">
            <svg viewBox="0 0 24 24" fill="none"><path d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M7 11l5 5 5-5M12 16V4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
            导出日志
          </button>
          <button class="btn btn-danger" @click="batchDelete">
            <svg viewBox="0 0 24 24" fill="none"><path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
            批量删除
          </button>
        </div>
      </div>

      <div class="stats-row">
        <div class="stat-card" style="--accent: #3b82f6;">
          <div class="stat-icon-wrap" style="background: #eff6ff; color: #3b82f6;">
            <svg viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M8 12h8M8 8h8M8 16h5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ todayCount }}</div>
            <div class="stat-label">今日交互</div>
          </div>
        </div>
        <div class="stat-card" style="--accent: #22c55e;">
          <div class="stat-icon-wrap" style="background: #f0fdf4; color: #22c55e;">
            <svg viewBox="0 0 24 24" fill="none"><path d="M20 7L10 17l-5-5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ successRate }}%</div>
            <div class="stat-label">识别成功率</div>
          </div>
        </div>
        <div class="stat-card" style="--accent: #f59e0b;">
          <div class="stat-icon-wrap" style="background: #fffbeb; color: #f59e0b;">
            <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/><path d="M12 7v5l3 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ avgResponseTime }}ms</div>
            <div class="stat-label">平均响应</div>
          </div>
        </div>
        <div class="stat-card" style="--accent: #ef4444;">
          <div class="stat-icon-wrap" style="background: #fef2f2; color: #ef4444;">
            <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/><path d="M12 8v4M12 16h.01" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ failedCount }}</div>
            <div class="stat-label">失败次数</div>
          </div>
        </div>
        <div class="stat-card" style="--accent: #8b5cf6;">
          <div class="stat-icon-wrap" style="background: #f5f3ff; color: #8b5cf6;">
            <svg viewBox="0 0 24 24" fill="none"><path d="M12 2a7 7 0 017 7c0 4-3.5 7-7 9-3.5-2-7-5-7-9a7 7 0 017-7z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><circle cx="12" cy="9" r="2.5" stroke="currentColor" stroke-width="1.4"/></svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ importantLogs.length }}</div>
            <div class="stat-label">重要标记</div>
          </div>
        </div>
      </div>

      <div class="controls-row">
        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.6"/><path d="M20 20l-3-3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
          <input type="text" v-model="searchQuery" placeholder="搜索指令或回复内容...">
          <button v-if="searchQuery" class="clear-btn" @click="searchQuery = ''">
            <svg viewBox="0 0 24 24" fill="none"><path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
          </button>
        </div>
        <select class="filter-select" v-model="filterDevice">
          <option value="all">全部设备</option>
          <option value="001">眼镜 #001</option>
          <option value="002">眼镜 #002</option>
          <option value="003">眼镜 #003</option>
        </select>
        <select class="filter-select" v-model="filterIntent">
          <option value="all">全部意图</option>
          <option value="navigation">导航</option>
          <option value="query">查询</option>
          <option value="control">控制</option>
          <option value="emergency">紧急</option>
        </select>
        <select class="filter-select" v-model="filterStatus">
          <option value="all">全部状态</option>
          <option value="success">成功</option>
          <option value="failed">失败</option>
        </select>
        <div class="result-count">共 {{ filteredLogs.length }} 条记录</div>
      </div>
    </div>

    <!-- Main content -->
    <div class="logs-content">
      <!-- Log list -->
      <div class="logs-list">
        <div v-if="filteredLogs.length === 0" class="empty-state">
          <svg viewBox="0 0 24 24" fill="none"><path d="M9 12h6M9 16h4M7 4H5a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2V8l-5-4H7z" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <p>暂无匹配的日志记录</p>
        </div>

        <div v-for="(group, date) in groupedLogs" :key="date" class="time-group">
          <div class="group-header" @click="toggleGroup(date)">
            <div class="group-title">
              <svg class="group-icon" viewBox="0 0 24 24" fill="none"><rect x="3" y="4" width="18" height="18" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M16 2v4M8 2v4M3 10h18" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
              <span class="group-text">{{ date }}</span>
              <span class="group-count">{{ group.length }} 条</span>
              <span class="group-success-rate">成功率 {{ groupSuccessRate(group) }}%</span>
            </div>
            <svg class="group-arrow" :class="{ rotated: expandedGroups[date] }" viewBox="0 0 24 24" fill="none"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </div>

          <div class="group-content" v-show="expandedGroups[date]">
            <div
              v-for="log in group"
              :key="log.id"
              :class="['log-card', log.status, { selected: selectedLogId === log.id, important: log.important }]"
              @click="selectLog(log)"
            >
              <!-- Intent badge + time -->
              <div class="log-header">
                <div class="log-badges">
                  <span :class="['intent-badge', log.intent]">{{ getIntentLabel(log.intent) }}</span>
                  <span :class="['status-badge', log.status]">
                    <svg viewBox="0 0 24 24" fill="none" v-if="log.status === 'success'"><path d="M20 7L10 17l-5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    <svg viewBox="0 0 24 24" fill="none" v-else><path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
                    {{ log.status === 'success' ? '成功' : '失败' }}
                  </span>
                  <span v-if="log.important" class="important-badge">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                    重要
                  </span>
                </div>
                <div class="log-time">
                  <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.4"/><path d="M12 7v5l3 3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
                  {{ formatTime(log.time) }}
                </div>
              </div>

              <!-- Chat bubbles -->
              <div class="log-bubbles">
                <div class="bubble user">
                  <div class="bubble-avatar user-avatar">
                    <svg viewBox="0 0 24 24" fill="none"><path d="M12 1a4 4 0 100 8 4 4 0 000-8zM4 20c0-4 3.582-7 8-7s8 3 8 7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
                  </div>
                  <div class="bubble-body user-body">
                    <div class="bubble-label">
                      <svg viewBox="0 0 24 24" fill="none"><path d="M12 2a3 3 0 00-3 3v6a3 3 0 006 0V5a3 3 0 00-3-3z" stroke="currentColor" stroke-width="1.4"/><path d="M19 10v1a7 7 0 01-14 0v-1M12 19v3M8 22h8" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
                      用户指令
                    </div>
                    <div class="bubble-text">{{ log.userCommand }}</div>
                  </div>
                </div>

                <div class="bubble system">
                  <div class="bubble-avatar system-avatar">
                    <svg viewBox="0 0 24 24" fill="none"><rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="1.4"/><circle cx="9" cy="10" r="1.5" fill="currentColor"/><circle cx="15" cy="10" r="1.5" fill="currentColor"/><path d="M8 14c1 1.5 6 1.5 8 0" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
                  </div>
                  <div class="bubble-body system-body">
                    <div class="bubble-label">
                      <svg viewBox="0 0 24 24" fill="none"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
                      系统响应
                    </div>
                    <div class="bubble-text">{{ log.systemResponse }}</div>
                  </div>
                </div>
              </div>

              <!-- Footer meta -->
              <div class="log-footer">
                <div class="log-meta">
                  <span class="meta-chip">
                    <svg viewBox="0 0 24 24" fill="none"><rect x="5" y="2" width="14" height="20" rx="2" stroke="currentColor" stroke-width="1.4"/><circle cx="12" cy="17" r="1" fill="currentColor"/></svg>
                    {{ log.device }}
                  </span>
                  <span class="meta-chip">
                    <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.4"/><path d="M12 7v5l3 3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
                    {{ log.duration }}ms
                  </span>
                  <span v-if="log.location" class="meta-chip">
                    <svg viewBox="0 0 24 24" fill="none"><path d="M12 22s-7-6.686-7-11.5a7 7 0 0114 0C19 15.314 12 22 12 22z" stroke="currentColor" stroke-width="1.4"/><circle cx="12" cy="10.5" r="2.5" stroke="currentColor" stroke-width="1.4"/></svg>
                    {{ log.location }}
                  </span>
                  <span class="meta-chip accuracy" :class="{ low: log.accuracy < 90 }">
                    <svg viewBox="0 0 24 24" fill="none"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" stroke="currentColor" stroke-width="1.4"/></svg>
                    准确率 {{ log.accuracy }}%
                  </span>
                </div>
                <div class="log-actions">
                  <button class="action-btn" @click.stop="playAudio(log)" title="播放语音">
                    <svg viewBox="0 0 24 24" fill="none"><polygon points="5,3 19,12 5,21" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
                  </button>
                  <button :class="['action-btn', { 'active-star': log.important }]" @click.stop="markImportant(log)" title="标记重要">
                    <svg viewBox="0 0 24 24" :fill="log.important ? 'currentColor' : 'none'"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
                  </button>
                  <button class="action-btn" @click.stop="analyzeLog(log)" title="分析详情">
                    <svg viewBox="0 0 24 24" fill="none"><path d="M18 20V10M12 20V4M6 20v-6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
                  </button>
                  <button class="action-btn" @click.stop="annotateLog(log)" title="添加标注">
                    <svg viewBox="0 0 24 24" fill="none"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
                  </button>
                  <button v-if="log.status === 'failed'" class="action-btn retry" @click.stop="retryLog(log)" title="重试">
                    <svg viewBox="0 0 24 24" fill="none"><path d="M1 4v6h6M3.51 15a9 9 0 102.13-9.36L1 10" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </button>
                </div>
              </div>

              <!-- Expanded detail -->
              <div class="log-details" v-if="selectedLogId === log.id">
                <div class="detail-grid">
                  <div class="detail-item">
                    <span class="detail-label">意图分类</span>
                    <span :class="['detail-value', 'intent-tag', log.intent]">{{ getIntentLabel(log.intent) }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">识别准确率</span>
                    <span class="detail-value">{{ log.accuracy }}%</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">置信度</span>
                    <span class="detail-value">{{ log.confidence }}%</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">响应耗时</span>
                    <span class="detail-value" :class="{ 'val-warn': log.duration > 2000 }">{{ log.duration }}ms</span>
                  </div>
                  <div v-if="log.error" class="detail-item detail-full">
                    <span class="detail-label">错误信息</span>
                    <span class="detail-value val-error">{{ log.error }}</span>
                  </div>
                  <div v-if="log.annotation" class="detail-item detail-full">
                    <span class="detail-label">标注说明</span>
                    <span class="detail-value">{{ log.annotation }}</span>
                  </div>
                </div>
                <div class="accuracy-bar-wrap">
                  <div class="accuracy-bar-label">识别准确率</div>
                  <div class="accuracy-bar">
                    <div class="accuracy-fill" :style="{ width: log.accuracy + '%' }" :class="{ low: log.accuracy < 90 }"></div>
                  </div>
                  <div class="accuracy-val">{{ log.accuracy }}%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Analysis panel -->
      <div class="analysis-panel">
        <!-- Success rate trend -->
        <div class="panel-card">
          <div class="panel-card-title">
            <svg viewBox="0 0 24 24" fill="none"><polyline points="22,12 18,12 15,21 9,3 6,12 2,12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
            识别成功率趋势（近7天）
          </div>
          <div class="trend-chart">
            <div class="trend-bars">
              <div v-for="(val, i) in successTrend" :key="i" class="trend-bar-wrap">
                <div class="trend-bar-value">{{ val }}%</div>
                <div class="trend-bar" :style="{ height: (val - 70) * 3.3 + 'px' }"></div>
                <div class="trend-bar-label">{{ trendLabels[i] }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Response time distribution -->
        <div class="panel-card">
          <div class="panel-card-title">
            <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M12 6v6l4 2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
            响应时间分布
          </div>
          <div class="pie-wrap">
            <div class="pie-chart"></div>
            <div class="pie-legend">
              <div class="legend-row">
                <span class="legend-dot" style="background:#22c55e"></span>
                <span class="legend-label">&lt;1s 快速</span>
                <span class="legend-pct">60%</span>
              </div>
              <div class="legend-row">
                <span class="legend-dot" style="background:#f59e0b"></span>
                <span class="legend-label">1~2s 正常</span>
                <span class="legend-pct">30%</span>
              </div>
              <div class="legend-row">
                <span class="legend-dot" style="background:#ef4444"></span>
                <span class="legend-label">&gt;2s 超时</span>
                <span class="legend-pct">10%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Top commands -->
        <div class="panel-card">
          <div class="panel-card-title">
            <svg viewBox="0 0 24 24" fill="none"><path d="M17 11H3M21 6H3M21 16H3M17 21H3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
            高频指令 TOP 5
          </div>
          <div class="top-commands">
            <div v-for="(cmd, i) in topCommands" :key="i" class="cmd-row">
              <span class="cmd-rank" :class="i < 3 ? 'top' : ''">{{ i + 1 }}</span>
              <span class="cmd-text">{{ cmd.text }}</span>
              <div class="cmd-bar-wrap">
                <div class="cmd-bar" :style="{ width: (cmd.count / topCommands[0].count * 100) + '%' }"></div>
              </div>
              <span class="cmd-count">{{ cmd.count }}次</span>
            </div>
          </div>
        </div>

        <!-- Failure reasons -->
        <div class="panel-card">
          <div class="panel-card-title">
            <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M12 8v4M12 16h.01" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
            常见失败原因
          </div>
          <div class="fail-reasons">
            <div v-for="(f, i) in failureReasons" :key="i" class="fail-row">
              <div class="fail-head">
                <span class="fail-name">{{ f.reason }}</span>
                <span class="fail-pct">{{ f.percent }}%</span>
              </div>
              <div class="fail-bar-bg">
                <div class="fail-bar-fill" :style="{ width: f.percent + '%' }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Intent distribution -->
        <div class="panel-card">
          <div class="panel-card-title">
            <svg viewBox="0 0 24 24" fill="none"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z" stroke="currentColor" stroke-width="1.6"/></svg>
            意图分类占比
          </div>
          <div class="intent-dist">
            <div v-for="(val, key) in intentDistribution" :key="key" class="intent-row">
              <span :class="['intent-dot', key]"></span>
              <span class="intent-name">{{ getIntentLabel(key) }}</span>
              <div class="intent-bar-bg">
                <div :class="['intent-bar-fill', key]" :style="{ width: val.percent + '%' }"></div>
              </div>
              <span class="intent-pct">{{ val.percent }}%</span>
            </div>
          </div>
        </div>

        <!-- Important logs -->
        <div class="panel-card">
          <div class="panel-card-title">
            <svg viewBox="0 0 24 24" fill="currentColor" style="color:#f59e0b"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            重要交互记录
          </div>
          <div v-if="importantLogs.length === 0" class="empty-mini">暂无重要标记</div>
          <div class="important-list">
            <div v-for="log in importantLogs" :key="log.id" class="imp-row" @click="selectLog(log)">
              <span :class="['imp-intent', log.intent]">{{ getIntentLabel(log.intent) }}</span>
              <span class="imp-text">{{ log.userCommand }}</span>
              <span class="imp-time">{{ formatTime(log.time) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Annotation modal -->
    <div class="modal-overlay" v-if="showAnnotationModal" @click="showAnnotationModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <div class="modal-title">
            <svg viewBox="0 0 24 24" fill="none"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
            标注失败原因
          </div>
          <button class="close-btn" @click="showAnnotationModal = false">
            <svg viewBox="0 0 24 24" fill="none"><path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>错误类型</label>
            <select v-model="annotation.errorType">
              <option value="recognition">识别错误</option>
              <option value="intent">意图理解错误</option>
              <option value="response">回复不合理</option>
              <option value="network">网络问题</option>
              <option value="other">其他</option>
            </select>
          </div>
          <div class="form-group">
            <label>详细说明</label>
            <textarea v-model="annotation.description" placeholder="请描述失败的具体原因..." rows="4"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showAnnotationModal = false">取消</button>
          <button class="btn btn-primary" @click="saveAnnotation">保存标注</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const searchQuery = ref('')
const filterIntent = ref('all')
const filterStatus = ref('all')
const filterDevice = ref('all')
const selectedLogId = ref(null)
const expandedGroups = ref({ '今天': true, '昨天': true })
const showAnnotationModal = ref(false)
const currentAnnotatingLog = ref(null)

const annotation = ref({ errorType: '', description: '' })

const logs = ref([
  {
    id: 1, time: Date.now() - 5 * 60 * 1000, device: '眼镜 #001',
    intent: 'navigation', status: 'success',
    userCommand: '帮我导航到最近的地铁站',
    systemResponse: '好的，正在为您规划到最近地铁站的路线，前方200米右转',
    duration: 1250, accuracy: 98, confidence: 95,
    error: null, errorType: null, annotation: null, location: '建国路88号', important: false
  },
  {
    id: 2, time: Date.now() - 18 * 60 * 1000, device: '眼镜 #001',
    intent: 'query', status: 'success',
    userCommand: '前面是什么建筑',
    systemResponse: '前方是北京国贸大厦，高228米，共74层',
    duration: 960, accuracy: 97, confidence: 94,
    error: null, errorType: null, annotation: null, location: '建国路88号', important: false
  },
  {
    id: 3, time: Date.now() - 30 * 60 * 1000, device: '眼镜 #001',
    intent: 'query', status: 'success',
    userCommand: '现在几点了',
    systemResponse: '现在是下午2点30分，天气晴，气温22度',
    duration: 890, accuracy: 99, confidence: 97,
    error: null, errorType: null, annotation: null, location: '建国路88号', important: false
  },
  {
    id: 4, time: Date.now() - 55 * 60 * 1000, device: '眼镜 #001',
    intent: 'navigation', status: 'success',
    userCommand: '前面是什么',
    systemResponse: '前方5米有红绿灯，现在是红灯，请等待',
    duration: 1100, accuracy: 96, confidence: 94,
    error: null, errorType: null, annotation: null, location: '建国路88号', important: true
  },
  {
    id: 5, time: Date.now() - 2 * 60 * 60 * 1000, device: '眼镜 #001',
    intent: 'control', status: 'failed',
    userCommand: '打开蓝牙',
    systemResponse: '抱歉，我没有理解您的指令，请重试',
    duration: 2100, accuracy: 85, confidence: 72,
    error: '指令识别失败', errorType: 'recognition', annotation: '环境噪音干扰较大', location: '建国路88号', important: false
  },
  {
    id: 6, time: Date.now() - 2.5 * 60 * 60 * 1000, device: '眼镜 #002',
    intent: 'emergency', status: 'success',
    userCommand: '救命，我摔倒了',
    systemResponse: '已检测到跌倒，正在紧急联系您的家人和救援人员，请保持冷静',
    duration: 800, accuracy: 100, confidence: 99,
    error: null, errorType: null, annotation: null, location: '王府井大街', important: true
  },
  {
    id: 7, time: Date.now() - 3 * 60 * 60 * 1000, device: '眼镜 #001',
    intent: 'query', status: 'failed',
    userCommand: '今天天气怎么样',
    systemResponse: '抱歉，网络连接超时，无法获取天气信息',
    duration: 3200, accuracy: 92, confidence: 88,
    error: '网络请求超时', errorType: 'network', annotation: null, location: '建国路88号', important: false
  },
  {
    id: 8, time: Date.now() - 3.5 * 60 * 60 * 1000, device: '眼镜 #003',
    intent: 'navigation', status: 'success',
    userCommand: '附近有没有公交站',
    systemResponse: '附近100米有国贸公交站，有1、4、10路等多条线路',
    duration: 1350, accuracy: 95, confidence: 93,
    error: null, errorType: null, annotation: null, location: '长安街', important: false
  },
  {
    id: 9, time: Date.now() - 24 * 60 * 60 * 1000 - 30 * 60 * 1000, device: '眼镜 #001',
    intent: 'navigation', status: 'success',
    userCommand: '带我去最近的超市',
    systemResponse: '好的，正在为您导航到附近的物美超市，距离约500米',
    duration: 950, accuracy: 97, confidence: 96,
    error: null, errorType: null, annotation: null, location: '建国路88号', important: false
  },
  {
    id: 10, time: Date.now() - 24 * 60 * 60 * 1000 - 2 * 60 * 60 * 1000, device: '眼镜 #001',
    intent: 'query', status: 'success',
    userCommand: '附近有什么餐厅',
    systemResponse: '附近有3家餐厅，最近的是全聚德烤鸭店，距离200米',
    duration: 1350, accuracy: 95, confidence: 93,
    error: null, errorType: null, annotation: null, location: '王府井', important: false
  },
  {
    id: 11, time: Date.now() - 24 * 60 * 60 * 1000 - 4 * 60 * 60 * 1000, device: '眼镜 #002',
    intent: 'control', status: 'success',
    userCommand: '调低音量',
    systemResponse: '音量已调整为50%',
    duration: 650, accuracy: 99, confidence: 98,
    error: null, errorType: null, annotation: null, location: '朝阳路', important: false
  },
  {
    id: 12, time: Date.now() - 24 * 60 * 60 * 1000 - 5 * 60 * 60 * 1000, device: '眼镜 #002',
    intent: 'query', status: 'failed',
    userCommand: '读一下这个牌子上的字',
    systemResponse: '抱歉，光线不足，无法识别文字',
    duration: 1800, accuracy: 76, confidence: 65,
    error: '图像识别失败', errorType: 'recognition', annotation: '环境光线过暗', location: '地铁站内', important: false
  }
])

const todayCount = computed(() => {
  const today = new Date(); today.setHours(0, 0, 0, 0)
  return logs.value.filter(l => l.time >= today.getTime()).length
})
const successCount = computed(() => logs.value.filter(l => l.status === 'success').length)
const failedCount = computed(() => logs.value.filter(l => l.status === 'failed').length)
const successRate = computed(() => logs.value.length === 0 ? 0 : Math.round(successCount.value / logs.value.length * 100))
const avgResponseTime = computed(() => {
  if (logs.value.length === 0) return 0
  return Math.round(logs.value.reduce((s, l) => s + l.duration, 0) / logs.value.length)
})

const filteredLogs = computed(() => {
  return logs.value.filter(log => {
    const q = searchQuery.value.toLowerCase()
    const searchMatch = !q || log.userCommand.toLowerCase().includes(q) || log.systemResponse.toLowerCase().includes(q)
    const intentMatch = filterIntent.value === 'all' || log.intent === filterIntent.value
    const statusMatch = filterStatus.value === 'all' || log.status === filterStatus.value
    const deviceMatch = filterDevice.value === 'all' || log.device.includes(filterDevice.value)
    return searchMatch && intentMatch && statusMatch && deviceMatch
  })
})

const groupedLogs = computed(() => {
  const groups = {}
  const today = new Date(); today.setHours(0, 0, 0, 0)
  const yesterday = new Date(today); yesterday.setDate(yesterday.getDate() - 1)
  filteredLogs.value.forEach(log => {
    const d = new Date(log.time)
    let key = d >= today ? '今天' : d >= yesterday ? '昨天' : d.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' })
    if (!groups[key]) groups[key] = []
    groups[key].push(log)
  })
  return groups
})

const importantLogs = computed(() => logs.value.filter(l => l.important).slice(0, 6))

const topCommands = computed(() => {
  const map = {}
  logs.value.forEach(l => {
    if (!map[l.userCommand]) map[l.userCommand] = { text: l.userCommand, count: 0 }
    map[l.userCommand].count++
  })
  return Object.values(map).sort((a, b) => b.count - a.count).slice(0, 5)
})

const failureReasons = computed(() => [
  { reason: '识别错误', percent: 45 },
  { reason: '网络问题', percent: 30 },
  { reason: '意图理解错误', percent: 15 },
  { reason: '其他', percent: 10 }
])

const intentDistribution = computed(() => ({
  navigation: { percent: 40 },
  query: { percent: 35 },
  control: { percent: 15 },
  emergency: { percent: 10 }
}))

const successTrend = computed(() => [85, 88, 92, 90, 87, 91, 94])
const trendLabels = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

const groupSuccessRate = (group) => {
  if (!group.length) return 0
  return Math.round(group.filter(l => l.status === 'success').length / group.length * 100)
}

const getIntentLabel = (intent) => ({ navigation: '导航', query: '查询', control: '控制', emergency: '紧急' }[intent] || '未知')

const formatTime = (ts) => new Date(ts).toLocaleString('zh-CN', { hour: '2-digit', minute: '2-digit' })

const toggleGroup = (date) => {
  expandedGroups.value[date] = !expandedGroups.value[date]
}

const selectLog = (log) => {
  selectedLogId.value = selectedLogId.value === log.id ? null : log.id
}

const exportLogs = () => { window.alert('正在导出日志，请稍候...') }
const batchDelete = () => { window.alert('请先选择要删除的日志记录') }
const playAudio = (log) => { window.alert(`正在播放 ${log.device} 的语音交互记录`) }
const markImportant = (log) => { log.important = !log.important }
const analyzeLog = (log) => { window.alert(`指令分析：\n意图：${getIntentLabel(log.intent)}\n准确率：${log.accuracy}%\n置信度：${log.confidence}%\n耗时：${log.duration}ms`) }
const retryLog = (log) => { window.alert(`正在重试指令：${log.userCommand}`) }

const annotateLog = (log) => {
  currentAnnotatingLog.value = log
  annotation.value = { errorType: log.errorType || '', description: log.annotation || '' }
  showAnnotationModal.value = true
}

const saveAnnotation = () => {
  if (currentAnnotatingLog.value) {
    currentAnnotatingLog.value.errorType = annotation.value.errorType
    currentAnnotatingLog.value.annotation = annotation.value.description
    showAnnotationModal.value = false
  }
}
</script>

<style scoped>
.logs {
  padding: 24px;
  background: #f1f5f9;
  min-height: calc(100vh - 52px);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Top box */
.logs-top-box {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.top-actions { display: flex; gap: 10px; }

.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.18s ease;
}
.btn svg { width: 15px; height: 15px; flex-shrink: 0; }
.btn-primary { background: #2563eb; color: #fff; }
.btn-primary:hover { background: #1d4ed8; box-shadow: 0 4px 12px rgba(37,99,235,0.35); }
.btn-secondary { background: #f8fafc; color: #334155; border: 1px solid #e2e8f0; }
.btn-secondary:hover { background: #f0f9ff; border-color: #bae6fd; color: #0369a1; }
.btn-danger { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
.btn-danger:hover { background: #fee2e2; }

/* Stats row */
.stats-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.stat-card {
  flex: 1;
  min-width: 130px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-left: 3px solid var(--accent);
}

.stat-icon-wrap {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.stat-icon-wrap svg { width: 18px; height: 18px; }

.stat-info { display: flex; flex-direction: column; gap: 3px; }
.stat-value { font-size: 20px; font-weight: 700; color: #1e293b; line-height: 1; }
.stat-label { font-size: 11px; color: #64748b; font-weight: 500; }

/* Controls row */
.controls-row {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 200px;
  max-width: 320px;
}
.search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: #94a3b8;
  pointer-events: none;
}
.search-box input {
  width: 100%;
  padding: 9px 36px 9px 34px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  color: #1e293b;
  background: #f8fafc;
  box-sizing: border-box;
}
.search-box input:focus { outline: none; border-color: #3b82f6; background: #fff; box-shadow: 0 0 0 3px rgba(59,130,246,0.1); }
.clear-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px; height: 20px;
  border: none; background: none; cursor: pointer; color: #94a3b8; padding: 0; display: flex; align-items: center; justify-content: center;
}
.clear-btn svg { width: 14px; height: 14px; }

.filter-select {
  padding: 9px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  color: #1e293b;
  background: #f8fafc;
  cursor: pointer;
}
.filter-select:focus { outline: none; border-color: #3b82f6; }

.result-count {
  font-size: 12px;
  color: #64748b;
  white-space: nowrap;
}

/* Main layout */
.logs-content {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 20px;
  align-items: start;
}

/* Log list */
.logs-list { display: flex; flex-direction: column; gap: 14px; }

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 48px;
  background: #fff;
  border-radius: 14px;
  color: #94a3b8;
}
.empty-state svg { width: 48px; height: 48px; }
.empty-state p { margin: 0; font-size: 14px; }

.time-group {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
  overflow: hidden;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 18px;
  background: linear-gradient(90deg, #f0f9ff 0%, #e0f2fe 100%);
  cursor: pointer;
  user-select: none;
}
.group-header:hover { background: linear-gradient(90deg, #dbeafe 0%, #bfdbfe 100%); }
.group-title { display: flex; align-items: center; gap: 10px; }
.group-icon { width: 16px; height: 16px; color: #3b82f6; flex-shrink: 0; }
.group-text { font-size: 15px; font-weight: 600; color: #1e293b; }
.group-count { font-size: 12px; color: #64748b; background: rgba(255,255,255,0.8); padding: 2px 8px; border-radius: 10px; }
.group-success-rate { font-size: 12px; color: #22c55e; font-weight: 600; }
.group-arrow { width: 16px; height: 16px; color: #64748b; transition: transform 0.2s; flex-shrink: 0; }
.group-arrow.rotated { transform: rotate(180deg); }

.group-content { padding: 10px 12px; display: flex; flex-direction: column; gap: 10px; }

/* Log card */
.log-card {
  background: #f8fafc;
  border-radius: 12px;
  padding: 14px 16px;
  cursor: pointer;
  transition: all 0.18s ease;
  border: 1px solid #e2e8f0;
  border-left: 3px solid #22c55e;
}
.log-card:hover { background: #fff; box-shadow: 0 4px 14px rgba(0,0,0,0.09); transform: translateY(-1px); }
.log-card.failed { border-left-color: #ef4444; }
.log-card.selected { background: #fff; box-shadow: 0 4px 16px rgba(59,130,246,0.15); border-color: #bfdbfe; }
.log-card.important { background: linear-gradient(135deg, #fffbeb 0%, #fef9c3 100%); border-color: #fde68a; }

/* Log header */
.log-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.log-badges { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }

.intent-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 6px;
}
.intent-badge.navigation { background: #dbeafe; color: #2563eb; }
.intent-badge.query { background: #dcfce7; color: #16a34a; }
.intent-badge.control { background: #fef3c7; color: #d97706; }
.intent-badge.emergency { background: #fee2e2; color: #dc2626; }

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 6px;
}
.status-badge svg { width: 11px; height: 11px; }
.status-badge.success { background: #dcfce7; color: #16a34a; }
.status-badge.failed { background: #fee2e2; color: #dc2626; }

.important-badge {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 11px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 6px;
  background: #fef3c7;
  color: #d97706;
}
.important-badge svg { width: 11px; height: 11px; }

.log-time {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #64748b;
}
.log-time svg { width: 13px; height: 13px; }

/* Bubbles */
.log-bubbles { display: flex; flex-direction: column; gap: 10px; margin-bottom: 12px; }

.bubble {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}
.bubble.user { flex-direction: row-reverse; }

.bubble-avatar {
  width: 30px; height: 30px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.bubble-avatar svg { width: 16px; height: 16px; }
.user-avatar { background: #dbeafe; color: #2563eb; }
.system-avatar { background: #f0fdf4; color: #16a34a; }

.bubble-body {
  max-width: 75%;
  border-radius: 12px;
  padding: 10px 14px;
}
.user-body { background: linear-gradient(135deg, #3b82f6, #2563eb); color: #fff; border-bottom-right-radius: 4px; }
.system-body { background: #fff; color: #1e293b; border: 1px solid #e2e8f0; border-bottom-left-radius: 4px; }

.bubble-label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 600;
  margin-bottom: 5px;
  opacity: 0.8;
}
.bubble-label svg { width: 12px; height: 12px; }
.bubble-text { font-size: 13px; line-height: 1.5; }

/* Footer */
.log-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid #e2e8f0;
  gap: 8px;
}
.log-meta { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }

.meta-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #64748b;
  background: #f1f5f9;
  padding: 3px 8px;
  border-radius: 6px;
}
.meta-chip svg { width: 12px; height: 12px; }
.meta-chip.accuracy { color: #22c55e; background: #f0fdf4; }
.meta-chip.accuracy.low { color: #f59e0b; background: #fffbeb; }

.log-actions { display: flex; gap: 6px; }

.action-btn {
  width: 30px; height: 30px;
  border: 1px solid #e2e8f0;
  border-radius: 7px;
  background: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  transition: all 0.15s ease;
  flex-shrink: 0;
}
.action-btn svg { width: 14px; height: 14px; }
.action-btn:hover { background: #f0f9ff; border-color: #bae6fd; color: #0369a1; }
.action-btn.active-star { color: #f59e0b; border-color: #fde68a; background: #fffbeb; }
.action-btn.retry { color: #3b82f6; border-color: #bfdbfe; }

/* Expanded detail */
.log-details {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #e2e8f0;
}
.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 12px;
}
.detail-item { display: flex; flex-direction: column; gap: 3px; }
.detail-full { grid-column: 1 / -1; }
.detail-label { font-size: 11px; color: #94a3b8; font-weight: 500; }
.detail-value { font-size: 13px; font-weight: 600; color: #1e293b; }
.detail-value.val-error { color: #ef4444; }
.detail-value.val-warn { color: #f59e0b; }

.intent-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 5px;
  font-size: 12px;
  font-weight: 600;
}
.intent-tag.navigation { background: #dbeafe; color: #2563eb; }
.intent-tag.query { background: #dcfce7; color: #16a34a; }
.intent-tag.control { background: #fef3c7; color: #d97706; }
.intent-tag.emergency { background: #fee2e2; color: #dc2626; }

.accuracy-bar-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}
.accuracy-bar-label { font-size: 11px; color: #64748b; white-space: nowrap; min-width: 56px; }
.accuracy-bar { flex: 1; height: 6px; background: #e2e8f0; border-radius: 3px; overflow: hidden; }
.accuracy-fill { height: 100%; background: #22c55e; border-radius: 3px; transition: width 0.3s; }
.accuracy-fill.low { background: #f59e0b; }
.accuracy-val { font-size: 12px; font-weight: 600; color: #1e293b; min-width: 36px; text-align: right; }

/* Analysis panel */
.analysis-panel {
  display: flex;
  flex-direction: column;
  gap: 14px;
  position: sticky;
  top: 72px;
  max-height: calc(100vh - 80px);
  overflow-y: auto;
}
.analysis-panel::-webkit-scrollbar { width: 4px; }
.analysis-panel::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 2px; }

.panel-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
  padding: 16px;
}

.panel-card-title {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 14px;
}
.panel-card-title svg { width: 15px; height: 15px; color: #3b82f6; flex-shrink: 0; }

/* Trend chart */
.trend-chart { padding: 0 4px; }
.trend-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 6px;
  height: 80px;
  padding-bottom: 20px;
  position: relative;
}
.trend-bar-wrap {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  height: 100%;
  justify-content: flex-end;
}
.trend-bar-value { font-size: 9px; color: #64748b; }
.trend-bar {
  width: 100%;
  max-width: 28px;
  background: linear-gradient(180deg, #60a5fa 0%, #3b82f6 100%);
  border-radius: 3px 3px 0 0;
  min-height: 4px;
  transition: height 0.3s;
}
.trend-bar-label { font-size: 9px; color: #94a3b8; margin-top: 4px; }

/* Pie chart */
.pie-wrap { display: flex; flex-direction: column; align-items: center; gap: 10px; }
.pie-chart {
  width: 90px; height: 90px;
  border-radius: 50%;
  background: conic-gradient(#22c55e 0% 60%, #f59e0b 60% 90%, #ef4444 90% 100%);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.pie-legend { width: 100%; display: flex; flex-direction: column; gap: 6px; }
.legend-row { display: flex; align-items: center; gap: 8px; }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.legend-label { flex: 1; font-size: 12px; color: #475569; }
.legend-pct { font-size: 12px; font-weight: 600; color: #1e293b; }

/* Top commands */
.top-commands { display: flex; flex-direction: column; gap: 8px; }
.cmd-row { display: flex; align-items: center; gap: 8px; }
.cmd-rank {
  width: 20px; height: 20px;
  border-radius: 5px;
  background: #e2e8f0;
  color: #64748b;
  font-size: 11px;
  font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.cmd-rank.top { background: linear-gradient(135deg, #fbbf24, #f59e0b); color: #fff; }
.cmd-text { font-size: 12px; color: #1e293b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 80px; flex: 1; }
.cmd-bar-wrap { flex: 1; height: 5px; background: #e2e8f0; border-radius: 3px; overflow: hidden; }
.cmd-bar { height: 100%; background: linear-gradient(90deg, #60a5fa, #3b82f6); border-radius: 3px; }
.cmd-count { font-size: 11px; color: #64748b; white-space: nowrap; }

/* Failure reasons */
.fail-reasons { display: flex; flex-direction: column; gap: 10px; }
.fail-row { display: flex; flex-direction: column; gap: 4px; }
.fail-head { display: flex; justify-content: space-between; align-items: center; }
.fail-name { font-size: 12px; color: #475569; }
.fail-pct { font-size: 12px; font-weight: 600; color: #ef4444; }
.fail-bar-bg { height: 5px; background: #fee2e2; border-radius: 3px; overflow: hidden; }
.fail-bar-fill { height: 100%; background: linear-gradient(90deg, #f87171, #ef4444); border-radius: 3px; }

/* Intent distribution */
.intent-dist { display: flex; flex-direction: column; gap: 8px; }
.intent-row { display: flex; align-items: center; gap: 7px; }
.intent-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.intent-dot.navigation { background: #3b82f6; }
.intent-dot.query { background: #22c55e; }
.intent-dot.control { background: #f59e0b; }
.intent-dot.emergency { background: #ef4444; }
.intent-name { font-size: 12px; color: #475569; min-width: 28px; }
.intent-bar-bg { flex: 1; height: 5px; background: #e2e8f0; border-radius: 3px; overflow: hidden; }
.intent-bar-fill.navigation { height: 100%; background: #3b82f6; border-radius: 3px; }
.intent-bar-fill.query { height: 100%; background: #22c55e; border-radius: 3px; }
.intent-bar-fill.control { height: 100%; background: #f59e0b; border-radius: 3px; }
.intent-bar-fill.emergency { height: 100%; background: #ef4444; border-radius: 3px; }
.intent-pct { font-size: 11px; color: #64748b; min-width: 30px; text-align: right; }

/* Important list */
.empty-mini { font-size: 12px; color: #94a3b8; text-align: center; padding: 8px 0; }
.important-list { display: flex; flex-direction: column; gap: 6px; }
.imp-row {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 7px 10px;
  border-radius: 8px;
  background: #fffbeb;
  cursor: pointer;
  transition: background 0.15s;
}
.imp-row:hover { background: #fef9c3; }
.imp-intent {
  font-size: 10px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
  flex-shrink: 0;
}
.imp-intent.navigation { background: #dbeafe; color: #2563eb; }
.imp-intent.query { background: #dcfce7; color: #16a34a; }
.imp-intent.control { background: #fef3c7; color: #d97706; }
.imp-intent.emergency { background: #fee2e2; color: #dc2626; }
.imp-text { flex: 1; font-size: 12px; color: #1e293b; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.imp-time { font-size: 11px; color: #94a3b8; white-space: nowrap; }

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.45);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
.modal {
  width: 90%;
  max-width: 460px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
  animation: modalIn 0.22s ease;
}
@keyframes modalIn {
  from { opacity: 0; transform: scale(0.92) translateY(16px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(90deg, #f0f9ff, #e0f2fe);
  border-radius: 16px 16px 0 0;
  border-bottom: 1px solid rgba(59,130,246,0.1);
}
.modal-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}
.modal-title svg { width: 18px; height: 18px; color: #3b82f6; }
.close-btn {
  width: 30px; height: 30px;
  border: none;
  border-radius: 6px;
  background: rgba(255,255,255,0.8);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  transition: all 0.15s;
}
.close-btn svg { width: 15px; height: 15px; }
.close-btn:hover { background: #fff; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
.modal-body { padding: 20px; display: flex; flex-direction: column; gap: 14px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 13px; font-weight: 600; color: #475569; }
.form-group select,
.form-group textarea {
  padding: 9px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  color: #1e293b;
  font-family: inherit;
  background: #f8fafc;
}
.form-group select:focus,
.form-group textarea:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59,130,246,0.1); }
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 14px 20px;
  border-top: 1px solid #e2e8f0;
  border-radius: 0 0 16px 16px;
}
</style>
