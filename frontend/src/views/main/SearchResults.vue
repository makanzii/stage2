<template>
  <div class="container py-3">
    <AskForGPT/>
    <a-list
        :bordered="false"
        :data="posts"
    >
      <template #item="{ item }">
        <a-list-item class="list-demo-item" action-layout="vertical">
          <router-link :to="`/discuss/${item.id}`">
            <div>
              <div class="d-flex flex-row align-items-center mb-2">
                <a-avatar :size="24">
                    <img :src="item.user.avatar"/>
                  </a-avatar>
                  <strong class="ms-1">{{item.user.username}}</strong>
                <span class="ms-1 me-1">·</span>
                <div class="small text-muted">{{ friendlyTime(item.created_at) }}</div>
              </div>
              <div>
                <h6> {{ item.title }}</h6>
              </div>
              <div>
                {{ item.content }}
              </div>
            </div>
          </router-link>

        </a-list-item>
      </template>
    </a-list>
  </div>
</template>
<script>
import server from "@/utils/api";
import {friendlyTime} from "@/utils/datetime";
import AskForGPT from "@/components/AskForGPT.vue";
export default {
  components:{AskForGPT},
  methods: {
    friendlyTime,
    async fetchChatResponse() {
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
  ,
  data() {
    return {
      chatResponse: '',
      keyword: "",
      gptLoading: false,
      gptVisible: false,
      posts: []
    }
  }
  ,
  mounted() {
    const keyword = this.$route.query.q
    this.keyword = keyword
    server.searchPostList(keyword).then(res => {
      this.posts = res.data.results
    })
  }
}
</script>
<style scoped>
a {
  text-decoration: none;
  color: inherit;
}

</style>
