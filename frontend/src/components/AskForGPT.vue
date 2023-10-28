<template>
  <div class="mb-2">
    <a-input-search :disabled="gptLoading" :loading="gptLoading" @search="fetchChatResponse" :style="{width:'500px'}"
                    v-model="keyword"
                    button-text="Ask"
                    search-button/>
  </div>
  <div v-if="gptVisible" class="gpt-answer">
    <div class="text-container">{{ chatResponse }}</div>
  </div>
</template>
<script>
import server from "@/utils/api";

export default {
  data() {
    return {
      gptVisible: false,
      chatResponse: '',
      gptLoading: false,
      keyword: ''
    }
  },
  methods: {
    async fetchChatResponse() {
      this.gptVisible=true
      this.gptLoading = true
      this.chatResponse = ''
      try {
        const responseStream = await server.createChat({input: this.keyword});

        const reader = responseStream.getReader();
        const decoder = new TextDecoder('utf-8');
        const readStream = async () => {
          const {done, value} = await reader.read();
          if (done) {
            this.gptLoading = false
            return;
          }
          const s = decoder.decode(value)
          this.chatResponse += s;
          return readStream();  // Recursively read the next chunk
        };

        await readStream();

      } catch (error) {
        console.error("Error fetching chat data:", error);
      }
    }
  }
}
</script>
<style>
.gpt-answer {
  min-height: 600px;
  background-color: #f7f7f7;
  border-radius: 10px;
  padding: 10px;
  overflow-y: auto;
}

.text-container {
  white-space: pre-line;
  word-wrap: break-word;
}
</style>
