<template>
  <div class="container py-3">
    <a-modal hide-cancel hide-ok ok-text="confirm" v-model:visible="studyPlanVisible" @ok="handleOk">
      <template #title>
        Your Study Plan
      </template>
      <div>
        <strong>Time Allocation</strong>
        <div>
          <a-typography-paragraph>
            <ul>
              <li>Duration: 8 weeks</li>
              <li> Per Week: Study 5 days</li>
              <li> Per Day: Suggested 1-2 hours of study</li>
            </ul>
          </a-typography-paragraph>
        </div>
        <strong>Content Plan</strong>
        <div class="mb-3">
          <div>Week 1 - Java Fundamentals</div>
          <div>Week 2 - Object-Oriented Basics</div>
          <div>Week 3 - Java Core Libraries</div>
          <div>Week 4 - Advanced Object-Oriented and Design</div>
          <div>Week 5 - File and I/O</div>
          <div>Week 6 - Multithreading and Concurrency</div>
          <div>Week 7 - Network Programming and Database Connectivity</div>
          <div>Week 8 - Integrated Practice and Advanced Topics</div>
        </div>
        <strong>Additional Content</strong>
        <div>
          <a-typography-paragraph>
            <ul>
              <li>Java Frameworks like Spring and Hibernate</li>
              <li>Basics of Java Web Development</li>
              <li>Tips on Java Performance Optimization and Debugging</li>
            </ul>
          </a-typography-paragraph>
        </div>
      </div>
    </a-modal>
    <div class="course-title">
      <h2>{{ course.title }}</h2>
    </div>
    <div class="small mb-2 text-muted">
      <div>Date: {{ course['start_time'] }} ~ {{ course['end_time'] }}</div>
    </div>
    <div class="mb-3">
      <a-tag :color="course.monday?'green':''">Mon.</a-tag>
      <a-tag :color="course.tuesday?'green':''">Tues.</a-tag>
      <a-tag :color="course.wednesday?'green':''">Wed.</a-tag>
      <a-tag :color="course.thursday?'green':''">Thur.</a-tag>
      <a-tag :color="course.friday?'green':''">Fri.</a-tag>
      <a-tag :color="course.saturday?'green':''">Sat.</a-tag>
      <a-tag :color="course.sunday?'green':''">Sun.</a-tag>
    </div>
    <div>
      <a-button @click="()=>{this.studyPlanVisible=true}" v-if="course.enrolled" class="me-2" type="primary"
                shape="round">Study plan
      </a-button>
      <a-button v-if="!course.enrolled" @click="enrollCourse(course)" type="primary" shape="round">Enroll
      </a-button>
      <a-button v-if="course.enrolled" @click="dropCourse(course)" status="danger" shape="round">Drop
      </a-button>
    </div>
    <a-typography-title :heading="5">
      Quizzes
    </a-typography-title>
    <div class="quizzes ms-1 mt-2">
      <div v-for="quiz in course.quizzes">
        {{ quiz.name }}
        <a-divider direction="vertical"></a-divider>
        {{ quiz.description }}
        <a-divider direction="vertical"></a-divider>
        Start Time: {{ quiz.date }}
        <a-divider direction="vertical"></a-divider>
        <a-link :disabled="quiz.available" :href="`/quiz/${quiz.id}`">take quiz</a-link>
      </div>
    </div>
    <a-typography-title :heading="5">
      Description
    </a-typography-title>
    <div class="text-container">
      {{ course.description }}
    </div>


  </div>
</template>

<script>
import server from "@/utils/api";

export default {
  data() {
    return {
      studyPlanVisible: false,
      course: {
        title: '',
        description: '.',
        startTime: '10:00 AM',
        endTime: '12:00 PM',
      }
    };
  },
  methods: {
    handleOk() {
      this.studyPlanVisible = false;
    },
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
    },
  },
  mounted() {
    const courseId = this.$route.params.courseId;
    server.getCourseDetail(courseId).then(res => {
      this.course = res.data;
    });
  }
};
</script>

<style scoped>
.text-container {
  white-space: pre-line;
  word-wrap: break-word;
}
</style>
