class WebSocketService {
  constructor() {
    this.ws = null
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectInterval = 3000
    this.listeners = new Map()
    this.isConnected = false
  }

  connect(url) {
    try {
      this.ws = new WebSocket(url)
      
      this.ws.onopen = () => {
        console.log('WebSocket connected')
        this.isConnected = true
        this.reconnectAttempts = 0
        this.emit('connected')
      }

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          this.handleMessage(data)
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error)
        }
      }

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        this.emit('error', error)
      }

      this.ws.onclose = () => {
        console.log('WebSocket disconnected')
        this.isConnected = false
        this.emit('disconnected')
        this.attemptReconnect()
      }
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error)
      this.attemptReconnect()
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
      this.isConnected = false
    }
  }

  send(data) {
    if (this.ws && this.isConnected) {
      this.ws.send(JSON.stringify(data))
    } else {
      console.warn('WebSocket is not connected')
    }
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, [])
    }
    this.listeners.get(event).push(callback)
  }

  off(event, callback) {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event)
      const index = callbacks.indexOf(callback)
      if (index > -1) {
        callbacks.splice(index, 1)
      }
    }
  }

  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => {
        callback(data)
      })
    }
  }

  handleMessage(data) {
    switch (data.type) {
      case 'device_status':
        this.emit('device_status', data.payload)
        break
      case 'video_frame':
        this.emit('video_frame', data.payload)
        break
      case 'location_update':
        this.emit('location_update', data.payload)
        break
      case 'alert':
        this.emit('alert', data.payload)
        break
      case 'voice_log':
        this.emit('voice_log', data.payload)
        break
      case 'heartbeat':
        this.emit('heartbeat', data.payload)
        break
      default:
        this.emit('message', data)
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`)
      setTimeout(() => {
        this.connect(this.url)
      }, this.reconnectInterval)
    } else {
      console.error('Max reconnection attempts reached')
      this.emit('max_reconnect_attempts_reached')
    }
  }

  subscribeToDevice(deviceId) {
    this.send({
      type: 'subscribe',
      payload: {
        device_id: deviceId,
        channels: ['status', 'video', 'location', 'alerts', 'voice_logs']
      }
    })
  }

  unsubscribeFromDevice(deviceId) {
    this.send({
      type: 'unsubscribe',
      payload: {
        device_id: deviceId
      }
    })
  }
}

export default new WebSocketService()
