<script setup>
import { ref } from "vue";
import axios from "axios";

// 定义响应式数据
const textInput = ref(""); // 用户输入的文本
const audioSrc = ref(null); // 播放音频的 URL
const isLoading = ref(false); // 是否正在加载中
const errorMessage = ref(""); // 错误信息

// 后端 API 的基础 URL
const BACKEND_BASE_URL = "http://localhost:8000";

/**
 * 生成语音的函数
 */
const generateAudio = async () => {
  // 重置状态
  audioSrc.value = null;
  errorMessage.value = "";
  isLoading.value = true;

  if (!textInput.value.trim()) {
    errorMessage.value = "Please enter some text to generate audio.";
    isLoading.value = false;
    return;
  }

  try {
    // 发送 POST 请求到后端 API
    const response = await axios.post(`${BACKEND_BASE_URL}/tts/generate`, {
      text: textInput.value,
    });

    // 检查响应是否包含 audio_url
    if (response.data && response.data.audio_url) {
      // 拼接完整的音频 URL
      audioSrc.value = `${BACKEND_BASE_URL}${response.data.audio_url}`;
      console.log("Generated Audio URL:", audioSrc.value);
    } else {
      errorMessage.value = "Backend did not return an audio URL.";
    }
  } catch (error) {
    console.error("Error generating audio:", error);
    errorMessage.value =
      "Failed to generate audio. Please check the backend server.";

    // 尝试从错误响应中获取更多细节
    if (error.response) {
      errorMessage.value += ` Status: ${error.response.status}.`;
      if (error.response.data && error.response.data.detail) {
        errorMessage.value += ` Detail: ${error.response.data.detail}`;
      }
    } else if (error.request) {
      errorMessage.value += " No response received from server.";
    } else {
      errorMessage.value += ` Request setup error: ${error.message}`;
    }
  } finally {
    isLoading.value = false; // 无论成功或失败，都结束加载状态
  }
};
</script>

<template>
  <div id="app">
    <h1>CosyVoice TTS Demo</h1>

    <div class="input-section">
      <textarea
        v-model="textInput"
        placeholder="Enter text here to convert to speech..."
        rows="5"
        :disabled="isLoading"
      ></textarea>
      <button @click="generateAudio" :disabled="isLoading">
        <span v-if="isLoading">Generating...</span>
        <span v-else>Generate Speech</span>
      </button>
    </div>

    <div v-if="errorMessage" class="message error">
      {{ errorMessage }}
    </div>

    <div v-if="audioSrc" class="audio-player-section">
      <h2>Generated Audio:</h2>
      <audio :src="audioSrc" controls autoplay></audio>
      <p>
        You can also
        <a :href="audioSrc" download="cosyvoice_audio.wav">download the audio</a
        >.
      </p>
    </div>

    <div v-if="isLoading && !errorMessage" class="message loading">
      Please wait, generating audio... This might take a moment.
    </div>
  </div>
</template>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #34495e;
  margin-bottom: 30px;
}

.input-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 30px;
}

textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
  resize: vertical;
  min-height: 120px;
  box-sizing: border-box; /* 确保 padding 和 border 不会增加宽度 */
}

button {
  padding: 12px 25px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover:not(:disabled) {
  background-color: #369f72;
}

button:disabled {
  background-color: #a0d9b5;
  cursor: not-allowed;
}

.message {
  padding: 10px 15px;
  border-radius: 6px;
  margin-top: 20px;
  font-weight: bold;
}

.error {
  background-color: #ffe0e0;
  color: #d32f2f;
  border: 1px solid #d32f2f;
}

.loading {
  background-color: #e0f7fa;
  color: #00796b;
  border: 1px solid #00796b;
}

.audio-player-section {
  margin-top: 30px;
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #eee;
  border-radius: 8px;
}

.audio-player-section h2 {
  color: #34495e;
  margin-bottom: 15px;
}

audio {
  width: 100%;
  margin-top: 15px;
}

a {
  color: #42b983;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
