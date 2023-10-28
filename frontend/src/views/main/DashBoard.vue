<script>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import server from "@/utils/api";

export default {
  components: {
    FullCalendar // make the <FullCalendar> tag available
  },
  data() {
    return {
      studyPlan: '',
      todayCourse: '',
      isGenerating: false,
      calendarOptions: {
        plugins: [dayGridPlugin],
        initialView: 'dayGridMonth',
        weekends: true,
        contentHeight: 700,
        events: [
          {title: 'Meeting', start: new Date()},
          {title: 'Meeting2', start: new Date()}
        ]
      }
    }
  },
  methods: {
    generateStudyPlan() {
      this.isGenerating = true
      server.generateStudyPlan().then(res => {
        this.studyPlan = res.data.studyPlan
        this.isGenerating = false
      })
    }
  },
  mounted() {
    server.getDashboard().then(res => {
      this.studyPlan = res.data.studyPlan
      this.calendarOptions.events = res.data.schedule
      this.todayCourse = res.data.todayCourse
    })
  }
}
</script>

<template>
  <main class="container py-3">
    <div class="d-flex flex-row justify-content-between">
      <FullCalendar style="width: 100%" :options='calendarOptions'/>
<!--      <div style="width: 380px">-->
<!--        <div class="study-plan">-->
<!--          <div class="study-plan-header  d-flex flex-row justify-content-between align-items-center">-->
<!--            <strong>Study plan</strong>-->
<!--            <a-button :disabled="isGenerating" :loading="isGenerating" @click="generateStudyPlan" shape="round"-->
<!--                      size="mini">-->
<!--              {{ studyPlan ? 'Regenerate' : 'Generate' }}-->
<!--            </a-button>-->
<!--          </div>-->
<!--          <div class="study-plan-content text-muted small text-container">-->
<!--            <div v-if="todayCourse">-->
<!--             <div>-->
<!--                <strong class="fs-6">Today's course</strong>-->
<!--             </div>-->
<!--              <div>-->
<!--                {{ todayCourse }}-->
<!--              </div>-->
<!--            </div>-->
<!--            &lt;!&ndash;            <span v-if="!studyPlan">you have no study plan yet 😄</span>&ndash;&gt;-->
<!--            &lt;!&ndash;            <span v-if="studyPlan">{{studyPlan}}</span>&ndash;&gt;-->
<!--          </div>-->
<!--        </div>-->

<!--      </div>-->
    </div>
  </main>
</template>

<style scoped>
.study-plan {
  border: 1px solid lightgray;
  border-radius: 10px;
}

.study-plan-header {
  border-radius: 10px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
  background-color: #4f8ff2;
  color: white;
  padding: 10px;
  width: 100%;
}

.study-plan-content {
  padding: 10px;
}

.text-container {
  white-space: pre-line;
  word-wrap: break-word;
}
</style>
