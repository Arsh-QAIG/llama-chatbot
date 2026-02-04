<script setup>
import { ref } from "vue";

const input = ref("");
const response = ref("");
const loading = ref(false);

async function sendPrompt() {
  if (!input.value.trim()) return;

  const prompt = input.value;
  response.value = "";
  loading.value = true;
  input.value = "";

  try {
    const res = await fetch("http://127.0.0.1:8000/chat/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });

    if (!res.body) return;

    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      response.value += decoder.decode(value);
    }
  } catch (err) {
    response.value += "\nError: " + (err.message || err);
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <main class="page">
    <div class="card">
      <h2 class="title">Q-Cluster Assistant</h2>

      <div class="chat">
        <div v-if="response" class="response">{{ response }}</div>
        <div v-else class="placeholder">Ask a question about Q-Cluster…</div>
      </div>

      <div class="input-row">
        <textarea
          v-model="input"
          rows="2"
          placeholder="Type your question…"
          class="textarea"
        />
        <button :disabled="loading" @click="sendPrompt" class="button">
          {{ loading ? "Thinking…" : "Send" }}
        </button>
      </div>
    </div>
  </main>
</template>

<style>
.page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #e5e7eb;
  padding: 16px;
}
.card {
  width: 100%;
  max-width: 640px;
  background: #fff;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}
.title {
  font-size: 20px;
  font-weight: 600;
  text-align: center;
  margin-bottom: 16px;
}
.chat {
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  background: #f9fafb;
  min-height: 120px;
}
.response {
  white-space: pre-wrap;
  color: #2563eb;
  font-size: 14px;
}
.placeholder {
  color: #111;
  font-size: 14px;
}
.input-row {
  display: flex;
  gap: 8px;
}
.textarea {
  flex: 1;
  resize: none;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 8px;
}
.button {
  padding: 8px 16px;
  border-radius: 12px;
  background: #2563eb;
  color: #fff;
  border: none;
}
.button:disabled {
  background: #93c5fd;
}
</style>
