<template>
  <main class="container py-3 d-flex flex-column align-items-center">
    <div style="width: 800px">
      <div class="mb-3">
        <a-button @click="handleClick" shape="round" type="outline">New Question</a-button>
      </div>
      <a-modal  v-model:visible="visible" hide-cancel hide-ok ok-text="submit" @ok="handleOk">
        <template #title>
          New Question
        </template>
        <div>
          <a-form :model="createForm">
            <a-form-item field="name" label="Question">
              <a-input v-model="createForm.title"/>
            </a-form-item>
            <a-form-item field="post" label="Content">
              <a-textarea placeholder="Please enter something" allow-clear v-model="createForm.content"/>
            </a-form-item>
          </a-form>
        </div>
      </a-modal>
      <a-list
          class="list-demo-action-layout"
          :bordered="false"
          :data="posts"
          @page-change="handlePageChange"
          :pagination-props="paginationProps"
      >
        <template #item="{ item }">
          <a-list-item class="list-demo-item" action-layout="vertical">
<!--            <template #actions>-->
<!--              <span>12 Reply</span>-->
<!--            </template>-->
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
  </main>
</template>

<script>
import server from "@/utils/api";
import {friendlyTime} from "@/utils/datetime";

export default {
  data() {
    return {
      visible: false,
      createForm: {
        title: '',
        content: ''
      },
      posts: [],
      paginationProps: {
        defaultPageSize: 10,
        total: 1
      }
    }
  },
  mounted() {
    this.getPostList()
  },
  methods: {
    friendlyTime,
    handlePageChange(page) {
      server.getPostList(page).then(res => {
        this.posts = res.data.results
        this.paginationProps.total = res.data.count
      })
    },
    getPostList() {
      server.getPostList().then(res => {
        this.posts = res.data.results
        this.paginationProps.total = res.data.count
      })
    },
    handleClick() {
      this.visible = true;
    },
    handleOk() {
      const {title, content} = this.createForm;
      if (title === '' || content === '') {
        this.$message.error('Please fill in the form');
        throw new Error('Please fill in the form');
      }
      server.createPost(this.createForm).then(res => {
        this.$message.success('Create success!');
        this.visible = false;
        this.createForm = {
          title: '',
          content: ''
        }
        this.getPostList()
      });
    },
    handleCancel() {
      this.visible = false;
    }

  }

}
</script>

<style scoped>
a {
  text-decoration: none;
  color: inherit;
}

.list-demo-action-layout .image-area {
  width: 183px;
  height: 119px;
  border-radius: 2px;
  overflow: hidden;
}

.list-demo-action-layout .list-demo-item {
  padding: 20px 0;
  border-bottom: 1px solid var(--color-fill-3);
}

.list-demo-action-layout .image-area img {
  width: 100%;
}

.list-demo-action-layout .arco-list-item-action .arco-icon {
  margin: 0 4px;
}
</style>

