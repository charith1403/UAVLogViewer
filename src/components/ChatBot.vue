<template>
  <div class="chat-container">
    <div class="chat-log">
      <div v-for="(msg, index) in messages" :key="index" :class="msg.role">
        <strong>{{ msg.role }}:</strong> {{ msg.content }}
      </div>
    </div>
    <div class="chat-input">
      <input
        v-model="userInput"
        @keyup.enter="sendMessage"
        placeholder="Ask me about the flight..."
      />
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script>
import { v4 as uuidv4 } from 'uuid'

export default {
    data () {
        return {
            sessionId: uuidv4(),
            userInput: '',
            messages: [],
            logId: 'log171.bin'
        }
    },
    methods: {
        async sendMessage () {
            if (!this.userInput) return

            const question = this.userInput
            this.messages.push({ role: 'user', content: question })

            const payload = {
                sessionId: this.sessionId,
                question,
                logId: this.logId
            }

            try {
                const response = await fetch('http://127.0.0.1:8000/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                })

                const data = await response.json()
                this.messages.push({
                    role: 'assistant',
                    content: data.answer || data.error || 'No response from server.'
                })
            } catch (err) {
                this.messages.push({
                    role: 'assistant',
                    content: 'Error contacting backend.'
                })
            }

            this.userInput = ''
        }
    }
}
</script>

<style scoped>
.chat-container {
  max-width: 600px;
  margin: 2rem auto;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 1rem;
  background: #f9f9f9;
}

.chat-log {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 1rem;
}

.user {
  text-align: right;
  color: blue;
}

.assistant {
  text-align: left;
  color: green;
}

.chat-input {
  display: flex;
  gap: 1rem;
}

input {
  flex: 1;
  padding: 0.5rem;
}

button {
  padding: 0.5rem 1rem;
}
</style>
