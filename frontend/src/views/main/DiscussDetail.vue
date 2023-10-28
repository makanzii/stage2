<template>
  <main class="container py-3 d-flex flex-column align-items-center">
    <div style="width: 800px">

      <div>
        <strong class="fs-5"> {{ post.title }}</strong>
      </div>
      <div class="d-flex flex-row align-items-center mb-2 mt-2">
        <a-avatar :size="24"><img v-if="post.user" :src="post.user.avatar"/></a-avatar>
        <strong class="ms-1">{{ post.user && post.user.username}}</strong>
        <span class="ms-1 me-1">·</span>
        <div class="small text-muted">{{ friendlyTime(post.created_at) }}</div>
      </div>
      <div>
        {{ post.content }}
      </div>
      <div class="w-100 mt-4">
        <a-textarea v-model="content" :auto-size="{ minRows: 4, maxRows: 4 }"
                    placeholder="Please enter your comment..."/>
        <div class="d-flex flex-row justify-content-end mt-2">
          <a-button @click="addReply" type="primary">Submit</a-button>
        </div>
      </div>
      <a-divider></a-divider>
      <div>
        <div v-for="reply in replyList" :key="`r${reply.id}`">
          <div class="d-flex flex-row align-items-center mb-2 mt-2">
            <a-avatar :size="24"><img v-if="reply.user" :src="reply.user.avatar" /></a-avatar>
            <strong class="ms-1">{{reply.user&&reply.user.username}}</strong>
            <span class="ms-1 me-1">·</span>
            <div class="small text-muted">{{ friendlyTime(reply.created_at) }}</div>
          </div>
          <div class="text-container">{{reply.content}}</div>
          <a-divider></a-divider>
        </div>

      </div>
    </div>

  </main>
</template>
<script>
import server from "@/utils/api";
import {friendlyTime} from "@/utils/datetime";

export default {
  data() {
    return {
      post: {},
      replyList: [],
      content: ''
    }
  },
  methods: {
    friendlyTime,
    addReply() {
      if (this.content === "") {
        this.$message.error("reply can not be blank!")
      }
      const data = {
        post: this.post.id,
        content: this.content
      }
      server.createReply(data).then((resp) => {
         this.getReplyList();
      })
    },
    getReplyList() {
      server.getReplyList(this.post.id).then(data => {
        this.replyList = data.data
      })
    }
  },

  mounted() {
    const postId = this.$route.params.postId;
    this.post.id = postId;
    server.getPostDetail(postId).then(res => {
      this.post = res.data;
    });
    this.getReplyList();

  }
}
</script>
<style scoped>
.text-container {
  white-space: pre-line;
  word-wrap: break-word;
}
</style>
