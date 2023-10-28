<template>
  <main class="container py-3">
    <div class="d-flex flex-row">
      <a-card v-for="course in courseList" :key="course.id" :style="{ width: '360px',marginRight:'20px' }">
        <template #actions>
          <a-button shape="round" @click="ev => {this.$router.push(`/course/${course.id}`)}">
            Detail
          </a-button>

          <a-button v-if="!course.enrolled" @click="enrollCourse(course)" type="primary" shape="round">Enroll
          </a-button>
          <a-button v-if="course.enrolled" @click="dropCourse(course)" status="danger" shape="round">Drop
          </a-button>
        </template>
        <template #cover>
          <div :style="{height: '204px',overflow: 'hidden' }"
          >
            <img
                :style="{ width: '100%', transform: 'translateY(-20px)' }"
                alt="dessert"
                src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a20012a2d4d5b9db43dfc6a01fe508c0.png~tplv-uwbnlip3yd-webp.webp"
            />
          </div>
        </template>
        <a-card-meta>
          <template #title>
            {{ course.title }}
          </template>
          <template #description>
            <a-typography-paragraph :ellipsis="{ rows: 2}">
              {{ course.description }}
            </a-typography-paragraph>
          </template>

        </a-card-meta>
      </a-card>
    </div>
  </main>
</template>

<script>
import {
  IconThumbUp,
  IconShareInternal,
  IconMore,
} from '@arco-design/web-vue/es/icon';
import server from "@/utils/api";

export default {
  components: {IconThumbUp, IconShareInternal, IconMore},
  data() {
    return {
      courseList: []
    }
  },
  methods: {
    enrollCourse(course) {
      server.enrollCourse(course.id).then(res => {
        course.enrolled = true
        this.$message.success("Enroll successfully!")
      })
    },
    dropCourse(course) {
      server.dropCourse(course.id).then(res => {
        course.enrolled = false
        this.$message.success("Drop successfully!")
      })
    }
  },
  mounted() {
    server.getCourseList().then(res => {
      this.courseList = res.data.results
    })
  }
};
</script>
<style scoped>
.icon-hover {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  transition: all 0.1s;
}

.icon-hover:hover {
  background-color: rgb(var(--gray-2));
}
</style>
